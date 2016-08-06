# -*- coding: utf-8 -*-
"""
    pip_services_runtime.errors.BadRequestError
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Bad request exception type
    
    :copyright: Digital Living Software Corp. 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .ErrorCategory import ErrorCategory
from .MicroserviceError import MicroserviceError

class BadRequestError(MicroserviceError):
    """
    Errors due to improper user requests, like missing or wrong parameters 
    """

    def __init__(self, *args):
        category = ErrorCategory.BadRequest
        component = args[0] if len(args) > 2 else None
        code = args[1] if len(args) > 2 else (args[0] if len(args) > 1 else None)
        message = args[2] if len(args) > 2 else (args[1] if len(args) > 1 else args[0])

        super(BadRequestError, self).__init__(category, component, code, message)
        self.with_status(400);
