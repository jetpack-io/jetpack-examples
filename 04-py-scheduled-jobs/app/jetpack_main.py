import os
import requests
from typing import Dict, Union
import jetpack
import json
from dotenv import load_dotenv
from jetpack import jetroutine
from fastapi import FastAPI, Response
from pydantic import BaseModel

load_dotenv()
app = FastAPI()
SLACK_URL = os.environ.get("SLACK_URL")
assert SLACK_URL is not None

class DelayModel(BaseModel):
    delay: int
    message: str


@app.get("/")
async def ready() -> Response:
    return Response(status_code=200)


@app.post("/delay")
async def delay(delayed_message: DelayModel) -> Dict[str, Union[str, int]]:
    task = await jetpack.schedule(print_message(delayed_message.message),
                                  delta=delayed_message.delay)
    return {"result": "Message scheduled successfully",
            "delay": delayed_message.delay}


@jetroutine
async def print_message(message: str) -> None:
    url = SLACK_URL
    payload = json.dumps({"text": message})
    headers = {"content-type": "application/json", "Accept-Charset": "UTF-8"}
    if url: 
        requests.post(url,data=payload,headers=headers)
    print({"delayedMessage": message})
