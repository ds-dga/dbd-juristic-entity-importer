FROM python:3.7-alpine

RUN mkdir /code
WORKDIR /code
copy . /code/

run pip install -U pip
run pip install -Ur pip.txt

RUN python main.py
