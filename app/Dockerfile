# Dockerfile содержит список инструкций для образа
# Image: список инструкций для всех программных пакетов в ваших проектах
# Container: экземпляр образа во время выполнения

# pull official base image
FROM python:3.11.0a3-alpine3.15

# set work directory
WORKDIR /usr/src/bot

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Устанавливаем зависимости для Postgre
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

ENTRYPOINT ["python3", "main.py"]