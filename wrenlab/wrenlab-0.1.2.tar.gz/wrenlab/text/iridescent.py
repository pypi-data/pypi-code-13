import wrenlab.ncbi.medline

class IRIDESCENT(object):
    def __init__(self, path="~/.cache/wrenlab/iridescent.db"):
        self._path = os.path.expanduser(path)
        self._cx = sqlite3.connect(self._path)
