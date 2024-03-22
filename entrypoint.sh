#!/bin/ash

echo "Apply database migrations"

python3 manage.py migrate --no-input 

gunicorn Vehicles.wsgi:application --bind 0.0.0.0:8000

exec "$@"