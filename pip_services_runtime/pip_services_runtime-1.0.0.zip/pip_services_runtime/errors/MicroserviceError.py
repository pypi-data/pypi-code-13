# -*- coding: utf-8 -*-
"""
    pip_services_runtime.errors.MicroserviceError
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Microservice exception type
    
    :copyright: Digital Living Software Corp. 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .ErrorCategory import ErrorCategory

class MicroserviceError(Exception):
    """
    Base class for all errors thrown by microservice implementation
    """

    category = ErrorCategory.UnknownError
    component = None
    code = 'Undefined'
    cause = None
    status = 500
    details = None
    correlation_id = None
    stack = None
    
    def __init__(self, category = ErrorCategory.UnknownError, component = None, code = 'Undefined', message = 'Unknown error'):
        super(MicroserviceError, self).__init__(message)
        
        self.category = category
        self.component = str(component) if component != None else None
        self.code = code
        self.message = message
        self.name = code
        
    def __str__(self):
        return self.message

    def to_json(self):
        return { 
            'category': self.category,
            'component': self.component,
            'code': self.code,
            'status': self.status,
            'details': self.details,
            'correlation_id': self.correlation_id,
            'cause': str(self.cause),
            'stack': self.stack
        }
        
    def for_component(self, component):
        self.component = str(component or '')
        return self
        
    def with_code(self, code):
        self.code = code or 'Undefined'
        self.name = code
        return self
        
    def with_cause(self, cause):
        self.cause = cause
        return self
        
    def with_status(self, status):
        self.status = status or 500
        return self
        
    def with_details(self, *details):
        self.details = details
        return self
        
    def with_correlation_id(self, correlation_id):
        self.correlation_id = correlation_id
        return self
                
    def with_stack(self, stack):
        self.stack = stack
        return stack

    def wrap(self, cause):
        if isinstance(cause, MicroserviceError):
            return cause
            
        self.with_cause(cause)
        return self

    @staticmethod
    def wrap_error(error, cause):
        if isinstance(cause, MicroserviceError):
            return cause
        
        error.with_cause(cause)
        return error
            
    @staticmethod
    def from_value(value):
        value = value if isinstance(value, dict) else dict(value)

        error = MicroserviceError(
            value['category'] if 'category' in value else None,
            value['component'] if 'component' in value else None,
            value['code'] if 'code' in value else None,
            value['message'] if 'message' in value else None
        ).with_status(value['status'])

        if 'cause' in value:
            error.with_cause(value['cause'])
        if 'correlation_id' in value:
            error.with_correlation_id(value['correlation_id'])
        if 'details' in value:
            error.with_details(value['details'])
        if 'stack' in value:
            error.with_stack(value['stack'])

        return error