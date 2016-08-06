# -*- coding: utf-8 -*-
"""
    pip_services_runtime.errors.__init__
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Errors module initialization
    
    :copyright: Digital Living Software Corp. 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

__all__ = [ \
    'ErrorCategory', 'MicroserviceError', 'BadRequestError', 'BuildError', \
    'CallError', 'ConfigError', 'ConflictError', 'ConnectionError', 'FileError', 'NotFoundError', \
    'StateError', 'UnauthorizedError', 'UnsupportedError', 'UnknownError' \
]

from .ErrorCategory import ErrorCategory
from .MicroserviceError import MicroserviceError
from .BadRequestError import BadRequestError
from .BuildError import BuildError
from .CallError import CallError
from .ConfigError import ConfigError
from .ConflictError import ConflictError
from .ConnectionError import ConnectionError
from .FileError import FileError
from .NotFoundError import NotFoundError
from .StateError import StateError
from .UnauthorizedError import UnauthorizedError
from .UnsupportedError import UnsupportedError
from .UnknownError import UnknownError
