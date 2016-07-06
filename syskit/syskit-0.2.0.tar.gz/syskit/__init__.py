# -*- coding: utf-8 -*-

"""System information for pedants

Syskit tries to provide a uniform API to system details across all
platforms.  It is a tough task to walk a fine line between a usable
platform-neutral API and still accurately providing platform specific
details.  But syskit tries.
"""

from __future__ import (absolute_import,
                        unicode_literals, print_function, division)

import sys

from syskit import _apipkg


__version__ = '0.2.0'


#: Our own platform identifier
platform = sys.platform
if platform.startswith('linux'):
    platform = 'linux'
elif platform.startswith('sunos'):
    platform = 'sunos'
elif platform.startswith('aix'):
    platform = 'aix'


_apispec = {

    # Exceptions
    'NoSuchProcessError': '._errors:NoSuchProcessError',
    'PermissionError': '._errors:PermissionError',
    'AttrNotAvailableError': '._errors:AttrNotAvailableError',
    'AttrPermissionError': '._errors:AttrPermissionError',

    # General code and helpers
    'TimeSpec': '._timespec:TimeSpec',
    'text': '._utils:text',

    # Host information
    'boottime': '._host:boottime',
    'uptime': '._host:uptime',
    'loadavg': '._host:loadavg',
    'cputimes': '._host:cputimes',
    'MemoryStats': '._host:memorystats',

    # Process information
    'procs': '._process:procs',
    'Process': '._process:Process',
    'ProcessStatus': '._process:ProcessStatus',

    # Internal compatibility and support code
    '_enum': '._enum34',
    # '_six': '._six',

    # Default implementations of internal ABCs
    'impl': {
        'HostInfo': '._host_{platform}:HostInfo',
        'MemoryStats': '._host_{platform}:MemoryStats',
        'ProcessTable': '._process_{platform}:ProcessTable',
        'ProcessCtl': '._process_{platform}:ProcessCtl',
        'ProcessAttrs': '._process_{platform}:ProcessAttrs',
    },

    # ABCs for implementing the internals
    'abc': {
        'HostInfoABC': '._host:HostInfoABC',
        'MemoryStatsABC': '._host:MemoryStatsABC',
        'ProcessTableABC': '._process:ProcessTableABC',
        'ProcessCtlABC': '._process:ProcessCtlABC',
        'ProcessAttrsABC': '._process:ProcessAttrsABC',
    }
}


if sys.version_info >= (3, 4):
    _apispec['_enum'] = 'enum'


def _fmtspec(spec, **kwargs):
    new = {}
    for k, v in spec.items():
        if isinstance(v, dict):
            new[k] = _fmtspec(v, **kwargs)
        else:
            new[k] = v.format(**kwargs)
    return new


_apipkg.initpkg(__name__,
                _fmtspec(_apispec, platform=platform),
                attr={'platform': platform})
