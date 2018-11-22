#!/bin/bash
. venv/bin/activate

# Ensure album names do not contain invalid characters (such as whitespace)
python3 scripts/rename_folders.py "$1"

# Scale down originals as huge resolutions aren't needed or displayed by pix3
scripts/scale_originals.sh "$1"

# Run exiftran on all pictures to auto-rotate correctly
find "$1" -type f -iname "*.jpg" -print0 | while IFS= read -r -d $'\0' f
do
  exiftran -a -i "$f"
done

# Ensure the webserver and uwsgi have full access to the album
chmod -R 777 album
