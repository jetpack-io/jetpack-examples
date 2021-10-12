import asyncio
import time
import random
from typing import Dict, List, Tuple
from jetpack import job
# from coin_toss import flip_coin
# from fibonacci import fibonacci
# from error_job import error_thrower
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


@job
async def flip_coin(label: str) -> str:
    flip = "heads" if random.randint(0, 1) == 0 else "tails"
    time.sleep(1)
    print(f'For Job {label}: {flip}')
    time.sleep(1)
    return flip

@job
async def fibonacci(n: int) -> int:
    if n < 0:
        print("Incorrect input")
        raise ValueError
    # First Fibonacci number is 0
    elif n == 0:
        return 0
    # Second Fibonacci number is 1
    elif n == 1:
        return 1
    else:
        r: Tuple[int, int] = await asyncio.gather(fibonacci(n - 1), fibonacci(n - 2))
        return r[0] + r[1]

@job
def error_thrower():
    raise TestError("This is a passed error")