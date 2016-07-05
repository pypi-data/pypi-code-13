from .RFC6455 import *
from .httpParser import *
from .wrapper import *

with open(__path__[0] + '/version', 'r') as r:
    __version__ = r.read()
