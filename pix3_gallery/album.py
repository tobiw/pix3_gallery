class Album:
    def __init__(self, path):
        self._path = path

    @property
    def name(self):
        return self._path.replace('_', ' ')

    @property
    def url(self):
        return self._path
