# pix3_gallery
https://github.com/tobiw/pix3_gallery

Based on the original pix photo gallery: http://pix.sourceforge.net/

pix3_gallery is a rewrite from scratch (rather than a fork) of "pix - simple web based gallery system".

# Features
* Templating through an HTML file (currently using custom placeholders but could use something like Jinja in the future)
* Different themes and styles through the use of CSS
* No database required: albums and pictures are directly ready from the underlaying file system
* No user management or user-modifiable content such as comments (for simplicity, this is a feature)

# Main differences to original pix
* pix is unmaintained (last release 2005)
* it uses an outdated version of Python2
* it uses a Python cgi script instead of a modern uwsgi socket
* it uses a cluttered hierarchy with all files stores in one root folder, which also means:
* pix never made it onto PyPI for installation through pip

# Improvements
* written from scratch using Python3.5
* uses a central JSON configuration file, no changes to source code required to set up a new instance of the gallery
* Uses baguetteBox.js JavaScript lightbox plugin for more dynamic display of images (github.com/feimosi/baguetteBox.js)
* proper package distribution to enable easy installation through pip

# Requirements
See requirements.txt for list of packages required. When installing the package distribution through pip, all required dependencies will be installed automatically.

* pillow: image processing library, used to generate smaller versions and thumbnails of pictures
* uswgi: interface to the web server

# Installation
Configuration files and scripts for FreeBSD rc.d and nginx are provided in etc/.

pix3 web app configuration can be found in pix3_gallery/config.py. The most important option to adjust is probably the album_path on the local file system.

uWSGI can be further configured within app.ini, e.g. number of processes, daemon-mode.

Settings that have to match across different config files and processes:
* uWSGI socket path: app.ini and nginx.conf
* album_path: config.py and nginx.conf
* location of pix3 installation in etc/rc.d/uwsgi

# Development
Use the following commands to run a development server (no need for an external webserver):
```virtualenv -p python3 venv
. venv/bin/activate
pip3 install -r requirements.txt
uwsgi --http :8080 --wsgi-file app.py --static-map "/static=./static" --static-map "/pic=/tmp/album"
```
