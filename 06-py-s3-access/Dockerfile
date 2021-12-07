FROM amd64/python:3.9-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./app /app
EXPOSE 8080

CMD ["uvicorn", "jetpack_main:app", "--host", "0.0.0.0", "--port", "8080"]
