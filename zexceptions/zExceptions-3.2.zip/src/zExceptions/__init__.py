##############################################################################
#
# Copyright (c) 2002 Zope Foundation and Contributors.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE
#
##############################################################################
"""General exceptions that wish they were standard exceptions

These exceptions are so general purpose that they don't belong in Zope
application-specific packages.
"""

import warnings

from zope.interface import implementer
from zope.interface.common.interfaces import IException
from zope.publisher.interfaces.http import (
    IHTTPException,
    IMethodNotAllowed,
)
from zope.publisher.interfaces import (
    IBadRequest,
    INotFound,
    IRedirect,
)
from zope.security.interfaces import IForbidden

from ._compat import builtins
from ._compat import class_types
from ._compat import string_types


status_reasons = {
    # Informational
    100: 'Continue',
    101: 'Switching Protocols',
    102: 'Processing',

    # Successful
    200: 'OK',
    201: 'Created',
    202: 'Accepted',
    203: 'Non-Authoritative Information',
    204: 'No Content',
    205: 'Reset Content',
    206: 'Partial Content',
    207: 'Multi-Status',
    226: 'IM Used',

    # Redirection
    300: 'Multiple Choices',
    301: 'Moved Permanently',
    302: 'Found',
    303: 'See Other',
    304: 'Not Modified',
    305: 'Use Proxy',
    307: 'Temporary Redirect',
    308: 'Permanent Redirect',

    # Client Error
    400: 'Bad Request',
    401: 'Unauthorized',
    402: 'Payment Required',
    403: 'Forbidden',
    404: 'Not Found',
    405: 'Method Not Allowed',
    406: 'Not Acceptable',
    407: 'Proxy Authentication Required',
    408: 'Request Time-out',
    409: 'Conflict',
    410: 'Gone',
    411: 'Length Required',
    412: 'Precondition Failed',
    413: 'Request Entity Too Large',
    414: 'Request-URI Too Large',
    415: 'Unsupported Media Type',
    416: 'Requested Range Not Satisfiable',
    417: 'Expectation Failed',
    418: "I'm a teapot",
    422: 'Unprocessable Entity',
    423: 'Locked',
    424: 'Failed Dependency',
    426: 'Upgrade Required',
    428: 'Precondition Required',
    429: 'Too Many Requests',
    451: 'Unavailable for Legal Reasons',
    431: 'Request Header Fields Too Large',

    # Server Error
    500: 'Internal Server Error',
    501: 'Not Implemented',
    502: 'Bad Gateway',
    503: 'Service Unavailable',
    504: 'Gateway Time-out',
    505: 'HTTP Version not supported',
    507: 'Insufficient Storage',
    510: 'Not Extended',
    511: 'Network Authentication Required',
}


@implementer(IHTTPException)
class HTTPException(Exception):
    body = None
    errmsg = 'Internal Server Error'
    status = 500

    def setBody(self, body):
        self.body = body

    def getStatus(self):
        return self.status

    def setStatus(self, status, reason=None):
        self.status = status
        if reason is None:
            reason = status_reasons.get(status, 'Unknown')
        else:
            reason = reason
        self.errmsg = reason

    def __call__(self, environ, start_response):
        headers = [('content-type', 'text/html;charset=utf-8')]
        if self.errmsg is not None:
            reason = self.errmsg
        reason = status_reasons[self.getStatus()]
        start_response(
            '%d %s' % (self.getStatus(), reason),
            headers)
        body = self.body
        if body is None:
            body = str(self)
        return [body]


@implementer(IBadRequest)
class BadRequest(HTTPException):
    errmsg = 'Bad Request'
    status = 400


@implementer(IException)
class InternalError(HTTPException):
    errmsg = 'Internal Server Error'
    status = 500


@implementer(INotFound)
class NotFound(HTTPException):
    errmsg = 'Not Found'
    status = 404


@implementer(IForbidden)
class Forbidden(HTTPException):
    errmsg = 'Forbidden'
    status = 403


@implementer(IMethodNotAllowed)
class MethodNotAllowed(HTTPException):
    errmsg = 'Method Not Allowed'
    status = 405


@implementer(IRedirect)
class Redirect(HTTPException):
    errmsg = 'Found'
    status = 302


def convertExceptionType(name):
    import zExceptions
    etype = None
    if name in builtins.__dict__:
        etype = getattr(builtins, name)
    elif hasattr(zExceptions, name):
        etype = getattr(zExceptions, name)
    if (etype is not None and
            isinstance(etype, class_types) and
            issubclass(etype, Exception)):
        return etype


def upgradeException(t, v):
    # If a string exception is found, convert it to an equivalent
    # exception defined either in builtins or zExceptions. If none of
    # that works, then convert it to an InternalError and keep the
    # original exception name as part of the exception value.
    if isinstance(t, string_types):
        warnings.warn(
            'String exceptions are deprecated starting '
            'with Python 2.5 and will be removed in a '
            'future release', DeprecationWarning, stacklevel=2)

        etype = convertExceptionType(t)
        if etype is not None:
            t = etype
        else:
            v = t, v
            t = InternalError
    return t, v

from zExceptions.unauthorized import Unauthorized  # noqa
