import asyncio
from typing import Dict, List 
from jetpack import cli
from starlette.responses import HTMLResponse
from coin_toss import flip_coin
from fibonacci import fibonacci
from error_job import error_thrower
from fastapi import FastAPI, Response


app = FastAPI()


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
            flip_coin("B-Tails"),
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
def error()-> HTMLResponse:
    try:
        error_thrower()
    except Exception as err:
        content=f"""
        <h1> {type(err).__name__} </h1>
        <p> {err} </p>
        """
        return HTMLResponse(content=content, status_code=500)


@app.get("/")
async def ready() -> Response:
    return Response(status_code=200)


cli.handle(app)