#!/bin/sh

set -e

python manage.py collectstatic --noinput

python manage makemigrations

python manage migrate

uwsgi --socket :8000 --master --enable-threads --module config.wsgi
