from PIL import Image

from .error import *

def load_image(fname):
    im = Image.open(fname)
    (w, h) = im.size
    if w != h:
        raise ImageNotSquareException
    return im
