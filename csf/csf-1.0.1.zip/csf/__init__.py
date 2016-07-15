# coding=utf8
import sys

if sys.version < "3":
    reload(sys)
    sys.setdefaultencoding("utf-8")

from .conf import config
from .api import *

__version__ = "1.0.1"
config.version = __version__