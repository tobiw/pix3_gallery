import os
import os.path
from .config import config
from .pic import Pic


class AlbumNotFoundError(Exception):
    pass


class AlbumPresenter:
    """
    View class for an album.
    It takes the model (Album) as an input and can generate various outputs for
    the web app. Any sub-album will generate a new AlbumPresenter.
    """
    def __init__(self, album):
        if not isinstance(album, Album):
            raise TypeError('album has to be of type Album')

        self._album = album

    def get_subalbum(self, album_name):
        """Creates a new AlbumPresenter instance for the given sub-album"""
        return AlbumPresenter(self._album.get_subalbum(album_name))

    def __repr__(self):
        return '{:s}({!r})'.format(self.__class__.__name__, self._album)

    def render_subalbums(self):
        """Render output for list of sub-albums"""
        return '<br>'.join('<a href="{url:s}">{name:s}</a>'.format(
                           url=a.url, name=a.name)
                           for a in self._album.albums)

    def render_pictures(self):
        """Render output for picture gallery"""
        # Start gallery div
        lines = ['<div class="baguetteBox gallery">']

        # Add images and links
        lines += ['<a href="{url:s}"><img src="{src:s}" alt="{alt:s}"/></a>'.format(
            url=p.web_image, src=p.thumb_image, alt=p.comment or '')
            for p in self._album._pics]

        # Close gallery div and run baguetteBox
        lines += [
            '</div>',
            '<script>window.onload = function() { baguetteBox.run(".baguetteBox"); };</script>'
        ]

        return '\n'.join(lines)

    def render_description(self):
        """Render output for album description"""
        return self._album.comment


class Album:
    """
    Data structure that loads and represents an album in the filesystem.
    Model and loading controller only, does not do any view functionality.
    """
    def __init__(self, path, recurse=True):
        """
        Initialises a new Album model instance.
        path is the filesystem path to the album (must be a folder).
        recurse is used to stop recursing into sub-folders.
        """
        self._path = path
        self._albums = []
        self._pics = []

        if not os.path.isdir(path):
            raise ValueError('Path "{:s}" must be a directory'.format(path))

        # Ensure there is no trailing slash on path
        if self._path[-1] == '/':
            self._path = self._path[:-1]

        if recurse:
            self._load_album()

    def get_subalbum(self, album_name):
        """Return the model instance for a sub-album of the current album."""
        for a in self._albums:
            if a.directory_name == album_name:
                return a
        raise AlbumNotFoundError(album_name)

    def _has_supported_picture_file_types(self, entry):
        return any(entry.lower().endswith('.' + ext)
                   for ext in config['supported_file_types'])

    def _load_album(self):
        """Load pictures and sub-albums of the current album and append to albums and pics lists."""
        for entry in os.listdir(self._path):
            if entry[0] == '.':  # special file or resized image file
                continue

            if '.' not in entry or self._has_supported_picture_file_types(entry):
                entry_path = os.path.join(self._path, entry)

                if os.path.isdir(entry_path):  # sub album
                    self._albums.append(Album(entry_path, recurse=True))
                elif os.path.isfile(entry_path):  # picture
                    self._pics.append(Pic(entry_path, self))

        # Sort albums and pictures by name
        if config['albums']['sort']['enable']:
            self._albums = sorted(self._albums,
                                  key=lambda a: a.name,
                                  reverse=config['albums']['sort']['reverse'] is True)
        if config['pictures']['sort']['enable']:
            self._pics = sorted(self._pics, key=lambda p: p.filename)

    def _remove_album_path(self, p):
        r = p.replace(config['album_path'], '')
        if r and r[0] == '/':
            r = r[1:]
        return r

    @property
    def directory_name(self):
        """Returns the album's directory name only (instead of full path), including parent album(s)"""
        return self._remove_album_path(self._path)

    @property
    def name(self):
        """Removes filesystem album root path and returns full pretty name of album"""
        return self.directory_name.replace('_', ' ') + ' ({:d})'.format(len(self))

    @property
    def url(self):
        """Generates the URL for the album (perma-link)"""
        return '/album/' + self.directory_name

    @property
    def albums(self):
        """Returns list of sub-albums"""
        return self._albums

    @property
    def comment(self):
        """Returns the album comment (start of meta file to empty line)"""
        lines = self.get_meta_file().splitlines()
        if not lines:
            return ''

        try:
            empty_line_index = lines.index('')
        except ValueError:  # could not find empty line, return full file
            empty_line_index = None  # slice :None will result in complete list

        return '<br>'.join(lines[:empty_line_index])

    def get_meta_file(self):
        """Reads and returns the contents of the .meta file in the album"""
        try:
            with open(self._path + '/.meta', 'r') as f:
                return f.read().strip()
        except IOError:
            return ''

    def __str__(self):
        return self.name

    def __repr__(self):
        return '{:s}({:s})'.format(self.__class__.__name__, self._path)

    def __len__(self):
        """Returns the total number of items in this album"""
        return len(self._pics) + len(self._albums)
