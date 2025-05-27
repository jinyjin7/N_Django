FROM python:3.12.4-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update && apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    netcat-openbsd \
    && pip install --upgrade pip

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt


COPY . /app/
COPY . .

