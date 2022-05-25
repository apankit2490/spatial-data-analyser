#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."
    echo "SQL_HOST: $SQL_HOST SQL_PORT: $SQL_PORT"

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 5
    done

    echo "PostgreSQL started"
fi

python manage.py flush --no-input
python manage.py migrate

exec "$@"