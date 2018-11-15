import os.path
import re
import time
from .album import Album, AlbumPresenter
from .config import config


RE_ALBUM = re.compile('^/album/([a-zA-Z0-9_\-/]+)$')


class Pix:
    def __init__(self):
        if not os.path.exists(config['album_path']):
            raise ValueError('album_path "{:s}" does not exist'.format(
                config['album_path']))

        # Create root album which will contain all the albums.
        # The presenter will not display the root album as an actual album item
        # but go straight to the subalbums.
        # Presenters for the subalbums get created when a request for a
        # specific album is received.
        self.root_album = Album(config['album_path'])
        self.album_presenter = AlbumPresenter(self.root_album)

    # /
    def get_root_output(self, template):
        template = template.replace('@breadcrumb@', '')
        template = template.replace('@albums@', self.album_presenter.render_subalbums())
        template = template.replace('@pics@', '')
        template = template.replace('@album-description@', '')
        return template

    def _get_subalbum_presenter(self, album_name):
        split_name = album_name.split('/')
        presenter = self.album_presenter  # start searching at root
        for i, n in enumerate(split_name):  # recurse through full album name
            presenter = presenter.get_subalbum('/'.join(split_name[:i + 1]))
            assert presenter is not None, 'No subalbum presenter found for "{}"'.format('/'.join(split_name[:i + 1]))
        return presenter

    @staticmethod
    def _get_breadcrums(album_name):
        """
        >>> Pix._get_breadcrums('')
        []
        >>> Pix._get_breadcrums('test_abc')
        [('test abc': '/album/test_abc')]
        >>> Pix._get_breadcrums('test_abc/xyz')
        [('xyz': '/album/test_abc/xyz'), ('test abc': '/album/test_abc')]
        """
        names = album_name.split('/')
        if not names or not names[0]:
            return []

        links = ['/album']  # initialize with URL base
        for w in names:
            links.append('{:s}/{:s}'.format(links[-1], w))
        del links[0]  # drop first item "/album"

        assert len(names) == len(links), 'len(names) [{}] != len(links) [{}]'.format(len(names), len(links))
        return zip([n.replace('_', ' ') for n in names], links)

    def _get_breadcrum_ahrefs(self, album_name):
        return '/'.join('<a href="{:s}">{:s}</a>'.format(l, n)
                        for n, l in self._get_breadcrums(album_name))

    # /<name> or /<subalbum>/<name>
    def get_album_output(self, template, album_name):
        presenter = self._get_subalbum_presenter(album_name)
        template = template.replace('@breadcrumb@', self._get_breadcrum_ahrefs(album_name))
        template = template.replace('@album-description@', presenter.render_description())
        template = template.replace('@albums@', presenter.render_subalbums())
        template = template.replace('@pics@', presenter.render_pictures())
        return template

    def do_routing(self, request_uri, template):
        """Returns HTTP response code and HTML output"""
        if request_uri == '/':
            # If in root, display all top-level albums.
            template = self.get_root_output(template)
        elif request_uri.startswith('/album/'):
            # If in album, display sub-albums.
            m = RE_ALBUM.match(request_uri)
            if not m:
                return ('404 Not found', 'Invalid album')
            else:
                template = self.get_album_output(template, album_name=m.group(1))
        else:
            return ('404 Not found', 'This is a static file which should be served by the webserver')

        return ('200 OK', template)

    def get_output(self, request_uri):
        with open('static/template.html', 'r') as f:
            template = f.read()

        # Start timing of site generation
        time_start = time.time()

        template = template.replace('@title@', config['title'])

        # Pass the template into the routing engine
        ret_code, template = self.do_routing(request_uri, template)

        # Fill in template placeholders that are independent of routing
        template = template.replace('@control@', '')
        template = template.replace('@web-pic@', '')
        template = template.replace('@comment@', '')

        time_to_render = float(time.time() - time_start)
        template = template.replace('@gen-time@', '{:.4f}'.format(time_to_render))
        return (ret_code, template)

        r = ['<h2>Albums ({:d} items)</h2>'.format(len(self.root_album))]
        for a in self.root_album.albums:
            r.append('<li><a href="{:s}">{:s}</a></li>'.format(
                a.url, a.name))

        return '<br>\n'.join(r)
