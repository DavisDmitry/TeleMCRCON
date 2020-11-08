FROM python:3.8-buster

COPY ./app /app

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

CMD python bot.py