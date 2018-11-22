#!/bin/bash
echo "Deleting web images"
find "$1" -type f -name ".web_*"
find "$1" -type f -name ".web_*" -exec rm {} +

echo "Deleting thumbnails"
find "$1" -type f -name ".thumb_*"
find "$1" -type f -name ".thumb_*" -exec rm {} +
