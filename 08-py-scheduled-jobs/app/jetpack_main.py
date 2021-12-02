import requests
from typing import Dict, Union
import jetpack
import json
from jetpack import function
from fastapi import FastAPI, Response
from pydantic import BaseModel

app = FastAPI()


class DelayModel(BaseModel):
    delay: int
    message: str


@app.get("/")
async def ready() -> Response:
    return Response(status_code=200)


@app.post("/delay")
async def delay(delayed_message: DelayModel) -> Dict[str, Union[str,int]]:
    task = await jetpack.schedule(slack_message(delayed_message.message),
                           delta=delayed_message.delay)
    return {"message": delayed_message.message,
            "delay": delayed_message.delay}

@function
async def slack_message(message: str) -> Dict[str,str]:
    url = "https://hooks.slack.com/services/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"
    payload = json.dumps({"text": message})
    headers = {"content-type": "application/json", "Accept-Charset": "UTF-8"}
    if url: 
        requests.post(url,data=payload,headers=headers)
    return {"delayedMessage": message}
