FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./app /app
EXPOSE 80

ENV FLASK_ENV="development" FLASK_APP="jetpack_main"

CMD ["flask", "run", "--host", "0.0.0.0", "--port", "80"]