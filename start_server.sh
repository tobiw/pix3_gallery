#!/bin/sh

DEVELOPMENT=1

APP=app.py
PORT=7777

. venv/bin/activate
cd pix3_gallery

if [ "$DEVELOPMENT" -eq 1 ]
then
  # Development
  uwsgi --http :$PORT --wsgi-file "$APP" --master --processes 4 --threads 2 --stats 127.0.0.1:7778
else
  # Production
  uwsgi --ini app.ini
  # nginx: uwsgi_pass unix:/.../app.sock
fi
