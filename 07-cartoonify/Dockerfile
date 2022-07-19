FROM amd64/python:3.9.9-slim

ENV JETPACK_ENTRYPOINT=/app/cartoonify

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

RUN pip install poetry

WORKDIR /app

COPY poetry.lock pyproject.toml *.whl /app/

RUN poetry install --no-interaction

# Not sure if this is best way to do this. We need jetpack-sdk to be in PATH
# but poetry by default creates venv.
RUN ln -s $(poetry env info --path)/bin/jetpack-sdk /bin/

COPY ./ /app

CMD ["poetry", "run", "start"]
