#!/bin/sh

DEVELOPMENT=1

APP=app.py
PORT=7777

. venv/bin/activate

if [ "$DEVELOPMENT" -eq 1 ]
then
  # Development
  uwsgi --http :$PORT --wsgi-file "$APP" --static-map "/=./static" --static-map "/pic=/tmp/album" --master --processes 4 --threads 2
else
  # Production
  uwsgi --ini app.ini
  # nginx: uwsgi_pass unix:/.../app.sock
fi
