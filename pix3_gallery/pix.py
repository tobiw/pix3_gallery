import os.path
import time
from .album import Album
from .config import config


class Pix:
    def __init__(self):
        if not os.path.exists(config['album_path']):
            raise ValueError('album_path "{:s}" does not exist'.format(
                config['album_path']))

        self.root_album = Album(config['album_path'])

    def get_output(self):
        with open('static/template.html', 'r') as f:
            template = f.read()

        time_start = time.time()

        template = template.replace('@title@', config['title'])
        template = template.replace('@breadcrumb@', '')
        template = template.replace('@albums@', '')
        template = template.replace('@pics@', '')
        template = template.replace('@control@', '')
        template = template.replace('@web-pic@', '')
        template = template.replace('@comment@', '')
        template = template.replace('@album-description@', '')
        template = template.replace('@meta@', '')
        template = template.replace('@gen-time@', str(time.time() - time_start))
        return template

        r = ['<h2>Albums ({:d} items)</h2>'.format(len(self.root_album))]
        for a in self.root_album.albums:
            r.append('<li><a href="{:s}">{:s}</a></li>'.format(
                a.url, a.name))

        return '<br>\n'.join(r)
