#!/bin/sh


echo "Waiting for postgres..."

while ! nc -z postgre 5432; do
  sleep 0.1
done

echo "PostgreSQL started"

echo "Waiting for elasticsearch..."

while ! nc -z elasticsearch 9200; do
  sleep 0.1
done

echo "Elasticsearch started"

echo "Waiting for kibana..."

while ! nc -z kibana 5601; do
  sleep 0.1
done

echo "Kibana started"

echo "Starting python"

pipenv run python manage.py run -h 0.0.0.0
