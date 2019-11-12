FROM python:3.7.4-alpine

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./Pipfile .
RUN pip install --upgrade pip pipenv && \
    pipenv install

COPY . .

CMD pipenv run python manage.py run -h 0.0.0.0
