FROM amd64/python:3.9-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt 

ENV SLACK_URL=https://hooks.slack.com/services/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

COPY ./app /app
EXPOSE 8080

CMD ["uvicorn", "jetpack_main:app", "--host", "0.0.0.0", "--port", "8080"]
