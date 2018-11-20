import os
import os.path
from PIL import Image
from .config import config


class Pic:
    """Handles an individual picture."""
    def __init__(self, path, album):
        if not path:
            raise ValueError('Invalid argument (path: {!r})'.format(path))
        if album is None:
            raise ValueError('Invalid argument (album: {!r})'.format(album))

        self._path = path.replace('//', '/')
        self._album = album
        self._size = None

    @staticmethod
    def _get_prefixed_path(path, prefix):
        """
        >>> Pic._get_prefixed_path('/tmp/test', '.web_')
        '/tmp/.web_test'
        """
        prepath, filename = path.rsplit('/', 1)
        return '{:s}/{:s}{:s}'.format(prepath, prefix, filename)

    @property
    def web_path(self):
        return self._get_prefixed_path(self._path, '.web_')

    @property
    def thumbnail_path(self):
        return self._get_prefixed_path(self._path, '.thumb_')

    def _get_resized_pic_path(self, prefix):
        filename_begin = self._path.rfind(os.sep) + 1
        return '{:s}.{:s}_{:s}'.format(
            self._path[:filename_begin], prefix, self._path[filename_begin:])

    @property
    def size(self):
        if self._size is None:
            self._size = Image.open(self._path).size
        return self._size

    def _generate_resized(self, new_name, new_size, crop):
        new_width, new_height = new_size

        original = Image.open(self._path)
        width, height = original.size

        if width < new_width or height < new_height:
            return self._path
        else:
            if os.path.exists(new_name):
                return new_name

        # Calculate new height with correct aspect ratio and scale image
        new_height = int((height * new_width) / width)
        new_image = original.resize(
            (new_width, new_height),
            resample=Image.ANTIALIAS)

        target_width, target_height = new_size
        if crop:
            if new_width > target_width or new_height > target_height:  # requires further cropping
                center_x, center_y = new_width // 2, new_height // 2
                new_image = new_image.crop((center_x - target_width // 2, center_y - target_height // 2,
                                            center_x + target_width // 2, center_y + target_height // 2))
        new_image.save(new_name)

        return new_name

    @property
    def web_image(self):
        """Generates a web-resized image and provides a URL to the file"""
        p = self._generate_resized(self.web_path, config['resize']['web'],
                                   crop=False)
        return p.replace(config['album_path'], '/pic')

    @property
    def thumb_image(self):
        """Generates a thumbnail-resized image and provides a URL to the file"""
        p = self._generate_resized(self.thumbnail_path,
                                   config['resize']['thumbnail'],
                                   crop=True)
        return p.replace(config['album_path'], '/pic')

    @property
    def name(self):
        # Replace '_' with ' ' (space) to make nicer looking names
        sep = self._path.rfind(os.sep)
        dot = self._path.rfind('.')
        return self._path[sep + 1:dot].replace('_', ' ')

    @property
    def filename(self):
        return self._path[self._path.rfind(os.sep) + 1:]

    @property
    def comment(self):
        meta = self._album.get_meta_file()
        if not meta:
            return

        lines = meta.splitlines()

        empty_line_index = lines.index('')

        for line in lines[empty_line_index + 1:]:  # only go through <filename>=<comment> lines
            assert '=' in line, line
            filename, comment = line.split('=', 1)
            if filename == self.filename:
                return comment
        return ''

    def __str__(self):
        return self._path

    def __repr__(self):
        return '{:s}({:s})'.format(self.__class__.__name__, self._path)
