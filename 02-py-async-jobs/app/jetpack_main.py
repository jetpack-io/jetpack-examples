import asyncio
import boto3
from typing import Dict, List
from coin_toss import flip_coin
from fibonacci import fibonacci
from error_job import error_thrower
from fastapi import FastAPI, Response
from fastapi.responses import HTMLResponse


app = FastAPI()

# Bump the cache

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


@app.get("/readyz")
def readyz() -> Response:
    return Response(status_code=200)


@app.get("/s3_download")
async def s3_download() -> HTMLResponse:
    s3 = boto3.resource('s3')
    s3.Bucket("lago-test-bucket").download_file("lago-test.html", "/tmp/lago-test.html")
    html_content = open("/tmp/lago-test.html").read()
    return HTMLResponse(content=html_content, status_code=200)


@app.get("/error")
def error():
    error_thrower()
