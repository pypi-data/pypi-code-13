#!/usr/bin/env python
#-*- coding: utf-8 -*-

class NilandException(Exception):
    def __init__(self, code=None, message=None):
        self.http_code = code
        Exception.__init__(self, message)

class BadRequestException(NilandException):
    def __init__(self, code, data):
        self.errors = data
        message = ''
        if len(data) > 0:
            for field, errors in data.iteritems():
                data[field] = '[%s] %s' % (field, ', '.join(errors))
            message = (' '.join([value for key, value in data.iteritems()]))
        NilandException.__init__(self, code, message)

class AuthenticationFailedException(NilandException):
    def __init__(self, code=None):
        NilandException.__init__(self, code)

class ForbiddenException(NilandException):
    def __init__(self, code=None):
        NilandException.__init__(self, code)

class NotFoundException(NilandException):
    def __init__(self, code=None):
        NilandException.__init__(self, code)
