# import os
import re

from webapp2 import exc as exceptions
from util import user_in_domain, is_dev_server

try:
    from google.appengine.api import users
except ImportError:
    users = None

RE_WHITESPACE = re.compile(r'^\s*$')


def isregex(q):
    return type(q) is type(RE_WHITESPACE)


def _inherit(method, target):
    target.__name__ = method.__name__
    target.__module__ = method.__module__
    target.__doc__ = method.__doc__


def require(*validators):
    """Apply assertions for a series of validator methods as decorators."""
    def wrapper(method):
        def validate(self, *args, **kwargs):
            for v in validators:
                rv = v(self, *args, **kwargs)
                message = "Precondition failed: %s" % v.__name__
                assert (rv is not False), message
            return method.__call__(self, *args, **kwargs)
        _inherit(method, validate)
        return validate
    return wrapper


def is_secure(self, *args, **kwargs):
    self.response.headers["X-Requires-HTTPS"] = "true"
    on_https = (self.request.scheme in ('https',))
    if not (is_dev_server() or on_https):
        message = "This resource must be requested via HTTPS"
        raise exceptions.HTTPBadRequest(message)


def is_loggedin(self, *args, **kwargs):
    if not (users and users.get_current_user()):
        message = "This resource requires an authenticated session"
        raise exceptions.HTTPUnauthorized(message)


def is_admin(self, *args, **kwargs):
    if not (users and users.get_current_user()):
        raise exceptions.HTTPUnauthorized
    if not (users and users.is_current_user_admin()):
        message = "This resources requires an administrative session"
        raise exceptions.HTTPForbidden(message)


def user_domain(*filters):
    filters = [f for f in filters if isinstance(f, basestring)]

    def UserDomainMatchFail(self, *args, **kwargs):
        user = (users and users.get_current_user())
        if not user:
            message = "This resource requires an authenticated session"
            raise exceptions.HTTPUnauthorized(message)
        email = user and user.email()
        for f in filters:
            if user_in_domain(email, f):
                return True
        raise exceptions.HTTPForbidden
    return UserDomainMatchFail


def match_header(header_name, header_value):
    if not isregex(header_value):
        header_value = re.compile(header_value)

    def HeaderMatchFail(self, *args, **kwargs):
        actual = self.request.headers.get(header_name, None)
        if (actual is None) or not bool(header_value.match(actual)):
            message = "This requires a valid %s header." % (header_name)
            raise exceptions.HTTPBadRequest(message)
    return HeaderMatchFail


def secure(func):
    return require(is_secure)(func)

