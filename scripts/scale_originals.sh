#!/bin/bash

MAX_WIDTH=2000
MAX_HEIGHT=2000

function pic_is_large()
{
  SIZE=`identify "$f" | sed 's/.* JPEG //' | sed 's/ .*//'`
  W=`echo $SIZE | sed 's/x.*//'`
  H=`echo $SIZE | sed 's/.*x//'`
  echo "$W x $H"

  if [[ $W -gt $MAX_WIDTH || $H -gt $MAX_HEIGHT ]]
  then
    return 1
  else
    return 0
  fi
}

find "$1" -type f -iname "*.jpg" -print0 | while IFS= read -r -d $'\0' f
do
  echo "$f"
  pic_is_large "$f"
  if [ $? -eq 1 ]
  then
    echo "mogrify 2000x ..."
    mogrify -scale 2000x "$f")
  fi
done
