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


@implementer(IHTTPException)
class HTTPException(Exception):
    pass


@implementer(IBadRequest)
class BadRequest(HTTPException):
    pass


@implementer(IException)
class InternalError(HTTPException):
    pass


@implementer(INotFound)
class NotFound(HTTPException):
    pass


@implementer(IForbidden)
class Forbidden(HTTPException):
    pass


@implementer(IMethodNotAllowed)
class MethodNotAllowed(HTTPException):
    pass


@implementer(IRedirect)
class Redirect(HTTPException):
    pass


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
