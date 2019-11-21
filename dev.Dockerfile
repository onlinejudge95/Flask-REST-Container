FROM python:3.7.5-alpine

RUN apk update && \
    apk add --virtual build-deps gcc python-dev musl-dev && \
    apk add postgresql-dev && \
    apk add netcat-openbsd

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

COPY ./Pipfile Pipfile
RUN pip install --upgrade pip pipenv && \
    pipenv install --dev

COPY ./entrypoint.sh entrypoint.sh
RUN chmod +x entrypoint.sh

COPY . .
