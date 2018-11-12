import os.path
import time
from .album import Album, AlbumPresenter
from .config import config


class Pix:
    def __init__(self):
        if not os.path.exists(config['album_path']):
            raise ValueError('album_path "{:s}" does not exist'.format(
                config['album_path']))

        self.root_album = Album(config['album_path'])
        self.root_album_presenter = AlbumPresenter(self.root_album)

    def get_output(self):
        with open('static/template.html', 'r') as f:
            template = f.read()

        time_start = time.time()

        template = template.replace('@title@', config['title'])
        template = template.replace('@breadcrumb@', '')
        template = template.replace('@albums@', self.root_album_presenter.render_subalbums())
        template = template.replace('@pics@', self.root_album_presenter.render_pictures())
        template = template.replace('@control@', '')
        template = template.replace('@web-pic@', '')
        template = template.replace('@comment@', '')
        template = template.replace('@album-description@', '')

        time.sleep(0.2)
        time_to_render = float(time.time() - time_start)
        template = template.replace('@gen-time@', '{:.4f}'.format(time_to_render))
        return template

        r = ['<h2>Albums ({:d} items)</h2>'.format(len(self.root_album))]
        for a in self.root_album.albums:
            r.append('<li><a href="{:s}">{:s}</a></li>'.format(
                a.url, a.name))

        return '<br>\n'.join(r)
