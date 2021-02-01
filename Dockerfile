FROM python:3.8

RUN useradd -m -s /bin/bash -U appuser

COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY app /app

WORKDIR app

USER appuser

ENTRYPOINT python main.py
