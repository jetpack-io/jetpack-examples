import asyncio
import time
import random
from typing import Dict, List, Tuple
from jetpack import cli
from coin_toss import flip_coin
from fibonacci import fibonacci
from error_job import error_thrower
from fastapi import FastAPI, Response
from fastapi.responses import HTMLResponse


app = FastAPI()

class TestError(Exception):
    def __init__(self, message):
        self.message = message


@app.get("/")
async def ready() -> Response:
    return Response(status_code=200)


@app.get("/diamond")
async def diamond() -> Dict[str, List[str]]:
    results: List[str] = []
    results += [await flip_coin("A")]

    if results[0] == "heads":
        results += await asyncio.gather(
            flip_coin("B-Head"),
            flip_coin("C-Head")
        )
    else:
        results += await asyncio.gather(
            flip_coin("B-Tail"),
            flip_coin("C-Tails")
        )

    results += [await flip_coin("D")]

    return {"results": results}


@app.get("/fibonacci/{n}")
async def fib(n: int) -> int:
    result: int = await fibonacci(n)
    print(result)
    return result


@app.get("/error")
def error():
    error_thrower()


cli.handle(app)