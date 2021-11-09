from fastapi import FastAPI
from jetpack import job, cli
import boto3
import time
from datetime import datetime
from starlette.responses import HTMLResponse, Response

app = FastAPI()


@app.get("/")
def ready() -> Response:
    return Response(status_code=200)


@app.get("/test_job")
async def start_job() -> HTMLResponse:
    content: str = html_test_job()
    return HTMLResponse(content=content, status_code=200)


@job
def html_test_job():
    time.sleep(3)
    print("I'm inside the job")
    return "<html> <body> <h1> Test </h1> </body> </html>"


@app.get("/s3_download")
async def s3_download() -> HTMLResponse:
    html_content = await s3_access_job()
    return HTMLResponse(content=html_content, status_code=200)


@job
async def s3_access_job() -> str:
    s3 = boto3.resource('s3')
    # Read Bucket in Jetpack Account
    bucketA = s3.Bucket("lago-test-bucket")
    # Read Bucket in Personal Account
    bucketB = s3.Bucket("jetpack-test-bucket")
    v_log = open("last_visit.txt", "x")
    v_log.write(str(datetime.now()))
    v_log.close()
    # Read a file from the Jetpack Account
    bucketA.download_file("lago-test.html", "/tmp/lago-test.html")
    # Write a file to the Personal Account
    bucketB.put_object(Key="last_visit.txt", Body=open("last_visit.txt", "rb"))
    html_content = open("/tmp/lago-test.html").read()
    return html_content

cli.handle(app)
