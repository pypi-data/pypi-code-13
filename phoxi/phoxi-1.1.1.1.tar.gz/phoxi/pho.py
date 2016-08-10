from sys import platform as _platform
import sys
import os

if _platform == "win32":
    thisDir = os.path.dirname(os.path.abspath(__file__))
    os.environ["PATH"] = os.environ["PATH"] + ";" + thisDir

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
