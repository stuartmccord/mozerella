FROM python:3.6.7-alpine3.6

LABEL maintainer="Stuart McCord <stuart.mccord@gmail.com>"

COPY requirements.txt /app/
WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app