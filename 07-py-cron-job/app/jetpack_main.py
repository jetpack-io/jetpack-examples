# type: ignore
from jetpack import cron
import requests
import json


@cron.repeat(cron.every().minute)
async def btc_cron_job():
    r = requests.get("https://api.coindesk.com/v1/bpi/currentprice.json").text
    data = json.loads(r)
    print("Getting BTC Price")
    price = data["bpi"]["USD"]["rate"]
    print("Latest Bitcoin Price:", price)
