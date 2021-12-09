import asyncio
import requests

from dotenv import load_dotenv
from fastapi import FastAPI, Response
from jetpack import function, cron
from os import environ

load_dotenv()
app = FastAPI()

@app.get("/")
def hello_world():
    return '<h1>Hello! You are currently in {0}</h1>'.format(
        environ.get("FLASK_ENV"))

@cron.repeat(cron.every(2).minutes)
async def schedule_poll():
  await poll_down_status_impl()

@app.get("/poll_down_status")
async def poll_down_status():
  await poll_down_status_impl()

async def poll_down_status_impl():
  print("starting poll_down_status")
  websites = ["https://twitter.com", "https://cnn.com", "https://downdetector.com"]
  awaitables = []
  for website in websites:
    awaitables.append(check_if_down(website))
  
  is_downs = await asyncio.gather(*awaitables)
  for is_website_down in is_downs:
    print(f"checked if down for {website}")
    if is_website_down[1]:
      website = is_website_down[0]
      notify_slack(website)
  return "done"

@function
async def check_if_down(website: str):
    r = requests.get(website)
    return (website, True)
    return (website, r.status_code == requests.codes.ok)

def notify_slack(website):
    webhook_env_var_name = "SLACK_WEBHOOK_URL_SUFFIX"
    url_suffix_value = environ.get(webhook_env_var_name)
    if url_suffix_value == None:
      raise Exception("Please set an environment variable {webhook_env_var_name} for the slack incoming webhook URL.")
    url = "https://hooks.slack.com/services/" + url_suffix_value
    payload = {"text":f"ALERT: {website} is down."}
    headers = {"content-type": "application/json", "Accept-Charset": "UTF-8"}
    response = requests.post(url, data=str(payload), headers=headers)
    print(f"Posted to slack. Response code is: {response.status_code}")

if __name__ == "__main__":
    app.run()
