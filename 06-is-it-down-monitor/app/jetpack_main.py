import asyncio
import random
import requests

from dotenv import load_dotenv
from fastapi import FastAPI, Response
from jetpack import function, cron
from os import environ

load_dotenv()
app = FastAPI()

# This cronjob monitors the list of websites to see if any are down.
@cron.repeat(cron.every(30).minutes)
async def schedule_poll():
  print("running cronjob schedule_poll")
  await poll_down_status_impl()

@function
async def poll_down_status_impl():
  print("starting poll_down_status")

  # List of websites we care about. This could be set in a configuration store
  # as well.
  websites = ["https://twitter.com", "https://cnn.com", "https://downdetector.com"]

  awaitables = []
  for website in websites:
    awaitables.append(check_if_down(website))
  
  is_downs = await asyncio.gather(*awaitables)
  
  notifications = []
  for is_website_down in is_downs:
    website = is_website_down[0]
    down_text = "down" if is_website_down[1] else "not down"
    print(f"checked if down for {website} and it is {down_text}.")
    if is_website_down[1]:
      notifications.append(notify_slack(website))
  
  await asyncio.gather(*notifications)
  return "done"

@function
async def check_if_down(website: str):
    r = requests.get(website)
    
    # The following line is useful for debugging
    # return (website, True if random.randint(0, 1) == 1 else False)

    return (website, r.status_code != requests.codes.ok)

@function
async def notify_slack(website):
    webhook_env_var_name = "SLACK_WEBHOOK_URL"
    url = environ.get(webhook_env_var_name)
    if url == None:
      raise Exception("Please set an environment variable {webhook_env_var_name} for the slack incoming webhook URL.")
    payload = {"text":f"ALERT: {website} is down."}
    headers = {"content-type": "application/json", "Accept-Charset": "UTF-8"}
    response = requests.post(url, data=str(payload), headers=headers)
    print(f"Posted to slack. Response code is: {response.status_code}")

# This endpoint is useful for debugging by triggering the cronjob on demand.
@app.get("/poll_down_status")
async def poll_down_status():
  await poll_down_status_impl()

if __name__ == "__main__":
    app.run()
