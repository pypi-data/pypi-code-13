from .__meta__ import __author__, __version__
from .base import LazyCLib as __LazyCLib
import os as __os


def __pyname(x):
    return x.split('.')[0].replace('-', '_').replace(' ', '_')

globals().update({
    __pyname(f): __LazyCLib(f)
    for f in __os.listdir(__os.getcwd())
    if f.endswith('.c')
})
