# -*- coding: utf-8 -*-
"""
    pip_services_runtime.errors.UnauthorizedError
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Unauthorized access exception type
    
    :copyright: Digital Living Software Corp. 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .ErrorCategory import ErrorCategory
from .MicroserviceError import MicroserviceError

class UnauthorizedError(MicroserviceError):
    """
    Access errors caused by missing user identity or security permissions
    """

    def __init__(self, *args):
        category = ErrorCategory.Unauthorized
        component = args[0] if len(args) > 2 else None
        code = args[1] if len(args) > 2 else (args[0] if len(args) > 1 else None)
        message = args[2] if len(args) > 2 else (args[1] if len(args) > 1 else args[0])

        super(UnauthorizedError, self).__init__(category, component, code, message)
        self.with_status(401);
