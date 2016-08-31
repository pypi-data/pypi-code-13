


from webapp2 import cached_property
from webapp2 import exc as exceptions
import webapp2

try:
    from google.appengine.api import users
except ImportError:
    users = None



import re


from .template import RequestHandler as TemplateRequestHandler
from .session import RequestHandler as SessionRequestHandler

from .jsonkit import json_encode, json_decode



def augment(instance, newBaseClass, promote=False):
    if promote:
        class derived(newBaseClass, instance.__class__):
            """monkey patch (promoted)"""
            pass
    else:
        class derived(instance.__class__, newBaseClass):
            """monkey patch (mixin)"""
            pass
    derived.__name__ = newBaseClass.__name__
    instance.__class__ = derived
    return instance


def adapt_request_params(request):
    if len(request.body) and request.content_type == 'application/json':
        return request.json_body
    return request.params


class BaseRequestHandler(webapp2.RequestHandler):
    """Override dispatch() to support returning response bodies as string."""

    def dispatch(self):
        result = super(BaseRequestHandler, self).dispatch()
        if isinstance(result, (basestring, str, unicode)):
            self.response.write(result)
        return self.response


class BaseRequest(webapp2.Request):

    # AppEngine defaults to WebOb 1.1.1, so some properties may be missing
    # if the application doesn't instruct AppEngine to load a newer version.
    # These include `json_body` and `remote_addr`, which are provided in
    # WebOb 1.2.3 and newer.

    # Shim to sniff for proxy headers
    @cached_property
    def remote_addr_allow_proxy(self):
        """Retrieve the IP of the request client."""
        addr = getattr(self, 'client_addr', None)
        if addr is None:
            addr = self.environ.get('REMOTE_ADDR', '')
            addr = self.environ.get('HTTP_X_FORWARDED_FOR', addr)
        return addr.split(',')[0].strip()

    @cached_property
    def hostname(self):
        """Retrieve the hostname of the server, per the client's request."""
        hostname = self.headers.get('Host', None)
        try:
            port_prefix = hostname.index(':')
            hostname = hostname[0:port_prefix]
        except ValueError:
            pass
        return hostname

    @cached_property
    def input(self):
        return adapt_request_params(self)


class BaseResponse(webapp2.Response):

    def cachable(self, seconds=10, public=True):
        props = {'seconds': int(seconds)}
        if public:
            props['public'] = True
        else:
            props['private'] = True
        self._cache_expires(**props)
        return True

    def write_json(self, data):
        """A convenience method for properly passing JSON data."""
        self.content_type = 'application/json'
        self.headers['X-Content-Handler'] = 'response.json'
        self.body = json_encode(data)

        # For some reason this won't actually filling the body.
        # self.json_body = data


def patch_request(request):
    """Attach useful features to the request..."""
    return augment(request, BaseRequest, promote=True)


def patch_response(response):
    """Attach useful features to the response..."""
    return augment(response, BaseResponse, promote=True)





class RequestHandler(BaseRequestHandler, TemplateRequestHandler, SessionRequestHandler):
    """Extensions on request handler base to enable:

        - Simpler access to user properties
        - Common template methods
        - CORS response authorization

    """

    def pivot(self, nextRequestHandlerClass):
        """ Initializes an alternate request handler with current state.
            Simplifies integration of logic between UI and API handlers.
        """
        return nextRequestHandlerClass(self.request, self.response)

    def cors_allow(self, origin="*"):
        self.response.headers.add_header('Access-Control-Allow-Origin', origin)

    @property
    def user(self):
        return (users and users.get_current_user())

