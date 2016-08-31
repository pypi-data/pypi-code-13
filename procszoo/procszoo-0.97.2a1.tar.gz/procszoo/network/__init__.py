import os
import sys

_pyroute2_module_available = False
_pyroute2_netns_available = False
try:
    import pyroute2
except ImportError:
    pass
else:
    _pyroute2_module_available = True

if _pyroute2_module_available:
    try:
        pyroute2.NetNS
    except AttributeError:
        pass
    else:
        _pyroute2_netns_available = True
