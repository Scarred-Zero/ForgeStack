# !/usr/bin/env bash

python3 manage.py collectstatic --noinput
python3 manage.py migrate --noinput
gunicorn -m guinicorn --bind 0.0.0.0:8000 --workers 3 forgestack.wsgi:application
