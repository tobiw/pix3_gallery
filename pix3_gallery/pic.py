import os
import os.path
from PIL import Image


class Pic:
    """Handles an individual picture."""
    def __init__(self, path):
        self._path = path.replace('//', '/')
        self._size = None

    @property
    def web_path(self):
        return '.web_' + self._path

    @property
    def thumbnail_path(self):
        return '.thumb_' + self._path

    def _get_resized_pic_path(self, prefix):
        filename_begin = self._path.rfind(os.sep) + 1
        return '{:s}.{:s}_{:s}'.format(
            self._path[:filename_begin], prefix, self._path[filename_begin:])

    @property
    def size(self):
        if self._size is None:
            self._size = Image.open(self._path).size
        return self._size

    def generate_resized(self, new_name, new_width, new_height):
        original = Image.open(self._path)
        width, height = original.size

        if width < new_width or height < new_height:
            return self._path
        else:
            if os.path.exists(new_name):
                return new_name

        new_height = (height * new_width) / width
        new_image = original.resize(
                (new_width, new_height),
                resample=Image.ANTIALIAS)
        new_image.save(new_name)

        return new_name

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
        if str(self) == '':
            return ''

        name_begin = self._path.rfind(os.sep)
        directory = self._path[:name_begin]

        meta_filename = '{:s}{:s}.meta'.format(directory, os.sep)
        if os.path.exists(meta_filename):
            with open(meta_filename, 'r') as f:
                comment_lines = [l for l in f.readlines() if '=' in l]

            for image_name, comment in [l.split('=') for l in comment_lines]:
                if image_name.strip() == self.filename:
                    return comment.strip()
        return ''

    def __str__(self):
        return self._path

    def __repr__(self):
        return '{:s}({:s})'.format(self.__class__.__name__, self._path)
