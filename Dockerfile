FROM python:3.9-slim-buster

RUN apt update && apt install -y git && apt-get clean
RUN python -m pip install Django Pillow autopep8

COPY . $APP_HOME
