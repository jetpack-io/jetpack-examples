import asyncio
from typing import List
from starlette.responses import FileResponse
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from send import send_brochure, EmailResult


app = FastAPI()

@app.get("/")
async def read_index():
    return FileResponse("public/index.html")

@app.post("/api/send")
async def send(emails: List[str]) -> List[EmailResult]:

    #results = []
    #for email in emails:
    #    results.append(await send(email))

    promises = []
    for email in emails:
        promises.append(send(email))

    results = await asyncio.gather(*promises)

    return results


async def send(email: str) -> EmailResult:

    try:
        return await send_brochure(email)
    except Exception as e:
        print(e)
        return EmailResult(email, success=False, duration=-1)

app.mount("/", StaticFiles(directory="public"), name="public")
