FROM python:3.12.7

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

WORKDIR /app

ENV PYTHONUNBUFFERED=1

COPY . .