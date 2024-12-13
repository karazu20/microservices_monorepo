#!/bin/bash
NAME="alejandría"
DJANGODIR=../../
PATH_ENV=../../.venv
NUM_WORKERS=16
DJANGO_WSGI_MODULE=wsgi.py
TIMEOUT=0
cd $DJANGODIR
source $PATH_ENV/bin/activate
exec gunicorn /DJANGO_WSGI_MODULE:app \
  --name $NAME \
  --workers $NUM_WORKERS \
  --timeout $TIMEOUT \
  --bind= :8080\
  --reload
