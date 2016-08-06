# -*- coding: utf-8 -*-
"""
    pip_services_runtime.errors.ConflictError
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Concurrency conflict exception type
    
    :copyright: Digital Living Software Corp. 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .ErrorCategory import ErrorCategory
from .MicroserviceError import MicroserviceError

class ConflictError(MicroserviceError):
    """
    Errors raised by conflict in object versions posted by user and stored on server.
    """

    def __init__(self, *args):
        category = ErrorCategory.ConflictError
        component = args[0] if len(args) > 2 else None
        code = args[1] if len(args) > 2 else (args[0] if len(args) > 1 else None)
        message = args[2] if len(args) > 2 else (args[1] if len(args) > 1 else args[0])

        super(ConflictError, self).__init__(category, component, code, message)
        self.with_status(409);
