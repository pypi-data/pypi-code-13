from sys import platform as _platform
import sys

if sys.version_info >= (3, 0):
    if _platform == "linux" or _platform == "linux2":
        from .phoPython3Linux import *
    elif _platform == "win32":
        from .phoPython3Win import *
else:
    if _platform == "linux" or _platform == "linux2":
        from phoPython2Linux import *
    elif _platform == "win32":
        from phoPython2Win import *
