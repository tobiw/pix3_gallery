import os
import os.path
from .config import config
from .pic import Pic


class Album:
    """
    Data structure that loads and represents an album in the filesystem.
    Model and loading controller only, does not do any view functionality.
    """
    def __init__(self, path, recurse=True):
        self._path = path
        self._albums = []
        self._pics = []

        if recurse:
            self._load_album()

    def _has_supported_picture_file_types(self, entry):
        return any(entry.lower().endswith('.' + ext)
                   for ext in config['supported_file_types'])

    def _load_album(self):
        for entry in os.listdir(self._path):
            if entry[0] == '.':  # special file or resized image file
                continue

            if '.' not in entry or self._has_supported_picture_file_types(entry):
                entry_path = os.path.join(self._path, entry)

                if os.path.isdir(entry_path):  # sub album
                    self._albums.append(Album(entry_path, recurse=True))
                elif os.path.isfile(entry_path):  # picture
                    self._pics.append(Pic(entry_path))

        # Sort albums and pictures by name
        if config['albums']['sort']['enable']:
            self._albums = sorted(self._albums,
                                  key=lambda a: a.name,
                                  reverse=config['albums']['sort']['reverse'] is True)
        if config['pictures']['sort']['enable']:
            self._pics = sorted(self._pics, key=lambda p: p.filename)

    @property
    def name(self):
        p = self._path.replace(config['album_path'], '').replace('_', ' ')
        if p[0] == '/':
            p = p[1:]
        return p + ' ({:d})'.format(len(self))

    @property
    def url(self):
        p = self._path.replace(config['album_path'], '')
        if p[0] == '/':
            p = p[1:]
        return 'album/' + p

    @property
    def albums(self):
        return self._albums

    def __str__(self):
        return self.name

    def __repr__(self):
        return '{:s}({:s})'.format(self.__class__.__name__, self._path)

    def __len__(self):
        """Returns the total number of items in this album"""
        return len(self._pics) + len(self._albums)
