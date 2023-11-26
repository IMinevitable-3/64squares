#!/bin/bash
until python3 -c "import psycopg2; psycopg2.connect(host='$DATABASE_URL', dbname='$DATABASE_NAME', user='$DATABASE_USER', password='$DATABASE_PASS')"; do
    >&2 echo "Postgres is unavailable - sleeping"
    sleep 3
done
python3 manage.py makemigrations && python3 manage.py migrate && python3 manage.py runserver 0.0.0.0:8000