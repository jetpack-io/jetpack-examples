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
    task = await jetpack.schedule(print_message(delayed_message.message),
                           delta=delayed_message.delay)
    return {"message": delayed_message.message,
            "delay": delayed_message.delay}

@function
async def print_message(message: str) -> None:
    print(json.dumps({"delayedMessage": message}))
