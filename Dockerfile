FROM python:3.9.7-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

RUN pip install --upgrade pip 
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .