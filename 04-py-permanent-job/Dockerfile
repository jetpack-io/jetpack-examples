FROM python:3.9-slim

WORKDIR /app

COPY requirements-torch.txt /app/requirements-torch.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements-torch.txt --find-links https://download.pytorch.org/whl/cpu/torch_stable.html

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt 

COPY ./app /app
EXPOSE 80

CMD ["python", "jetpack_main.py"]