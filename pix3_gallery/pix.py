import os.path
from .album import Album
from .config import config


class Pix:
    def __init__(self):
        if not os.path.exists(config['album_path']):
            raise ValueError('album_path "{:s}" does not exist'.format(
                config['album_path']))

        self._albums = [Album(config['album_path'] + '/test_123')]

    def get_output(self):
        r = ['<h2>Albums</h2>']
        for a in self._albums:
            r.append('<li><a href="{:s}">{:s}</a></li>'.format(
                a.name, a.url))

        return '<br>\n'.join(r)
