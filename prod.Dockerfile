FROM python:3.7.5-alpine

RUN apk update && \
    apk add --virtual build-deps gcc python-dev musl-dev && \
    apk add postgresql-dev && \
    apk add netcat-openbsd

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_ENV production
ENV APP_SETTINGS app.config.ProductionConfig

WORKDIR /usr/src/app

COPY ./requirements.txt .
RUN pip install --upgrade pip && \
    pip install --requirement requirements.txt

COPY . .

RUN adduser -D webuser
USER webuser

CMD gunicorn --bind 0.0.0.0:$PORT --log-config gunicorn.conf manage:app
