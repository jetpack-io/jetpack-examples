from asyncio.tasks import sleep
import uvicorn
import cv2
import asyncio
import hashlib
import requests

import numpy as np
from typing import Any, Dict

from fastapi import FastAPI
from fastapi.responses import FileResponse

from jetpack import function, cron


"""
Sample jetpack app that turns photo into a cartoon.
Heavily inspired by https://towardsdatascience.com/turn-photos-into-cartoons-using-python-bb1a9f578a7e
"""

app = FastAPI()

@app.get("/")
async def root() -> Dict[str, str]: 
    return {
        "message": "Hello cartoonify!",
    }
    
@app.get("/image/")
async def image(image_name: str):
    return FileResponse(image_name)


@app.get("/process")
async def process(image_url: str) -> Dict[str, str]:
  image_name = await process_image(image_url)
  return {
      "image_uri": f"/image?image_name={image_name}",
  }

async def process_image(image_url: str) -> str:
  dest = f"{hashlib.md5(image_url.encode('utf-8')).hexdigest()}.jpg"
  cartoon = await perform_image_processing(image_url, dest)
  cv2.imwrite(dest, cartoon)
  return dest

@function
async def perform_image_processing(image_url: str, dest: str) -> Dict[str, str]:
    arr = np.asarray(bytearray(requests.get(image_url).content), dtype=np.uint8)
    img = cv2.imdecode(arr, -1) # 'Load it as it is'

    line_size = 7
    blur_value = 7
    total_color = 9

    edges, img = await asyncio.gather(
      edge_mask(img, line_size, blur_value),
      color_quantization(img, total_color),
    )
    blurred = cv2.bilateralFilter(img, d=7, sigmaColor=200,sigmaSpace=200)
    cartoon = cv2.bitwise_and(blurred, blurred, mask=edges)

    return cartoon

@function
async def color_quantization(img, k):
  # Transform the image
  data = np.float32(img).reshape((-1, 3))

  # Determine criteria
  criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.001)

  # Implementing K-Means
  ret, label, center = cv2.kmeans(data, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
  center = np.uint8(center)
  result = center[label.flatten()]
  result = result.reshape(img.shape)
  return result

@function
async def edge_mask(img, line_size, blur_value):
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  gray_blur = cv2.medianBlur(gray, blur_value)
  edges = cv2.adaptiveThreshold(gray_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, line_size, blur_value)
  return edges

@cron.repeat(cron.every().monday.at("10:30:42"))
async def my_cron2() -> None:
  pass

def start():
    """Launched with `poetry run start` at root level"""
    uvicorn.run("cartoonify.main:app", host="0.0.0.0", port=8080, reload=True)
