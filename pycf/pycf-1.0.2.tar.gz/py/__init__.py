# $Id: __init__.py.in 575 2011-03-16 21:07:02Z pletzer $

# this is to allow from pylibcf import *
__all__ = ["libCFConfig"]

# expose all symbols defined in the configuration file
from pycf.libCFConfig import *

