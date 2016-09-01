from .fasttext import skipgram
from .fasttext import cbow
from .fasttext import load_model
from .fasttext import supervised

import os

dir_path = os.path.dirname(os.path.realpath(__file__))
version_path = os.path.join(dir_path, 'VERSION')

def _read_version():
    with open(version_path) as f:
        return f.read().strip()

__VERSION__ = _read_version()
