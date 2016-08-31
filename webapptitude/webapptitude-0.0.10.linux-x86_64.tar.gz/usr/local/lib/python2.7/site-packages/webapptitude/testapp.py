"""
Lightweight abstraction for HTTP API's, with simple test facility.
This emulates some parts of the `webtest` module, but relies solely
on Python's native `urllib2` module.

This is intended to facilitate warm-up logic in a development environment,
and testing API functionality in the application.

Usage:  (as a separate script)

    # access the application as a remote client.
    >>> app = testapp.Application('localhost', '8080')

    # create an account, asserting a 200 response
    >>> account = app.post('/account/', dict(name="test account"), expect=200)

    # read its resulting ID from response (JSON)
    >>> account_id = (account.body_json.get('account_id'))

    # construct a URL with that account_id
    >>> verify_url = '/account/{accountid}/verify'.format(accountid=account_id)

    # post to the subordinate URI
    >>> verify = app.post(verify_url, dict(confirm=True))

"""

import json
import urllib2
from urllib import urlencode


class Application(object):

    default_headers = [('Content-Type', 'application/json')]

    class Response(object):
        # Nested classes FTW.
        def __init__(self, data):
            self.status = data.getcode()
            self.url = data.geturl()
            self.info = data.info()
            self.body = data.read()

        def expect(self, status):
            assert (self.status == status), \
                ("Expected %d, got %d" % (status, self.status))

        def header(self, name):
            return self.info.get(name)

        @property
        def body_json(self):
            return json.loads(self.body)

    # init for Application
    def __init__(self, host=None, port=None):
        self.host = host
        self.port = port
        self.opener = urllib2.build_opener(urllib2.HTTPHandler)

    @classmethod
    def add_headers_to_req(self, request, *args, **opts):
        for name, value in args:
            request.add_header(name, value)
        for name, value in opts.items():
            request.add_header(name, value)


    def request(self, method, uri, data=None, headers=None):
        if method.upper() in ('GET', 'HEAD', 'DELETE'):
            data = data and urlencode(data) or ''
            uri = uri + '?' + data
            data = None
        else:
            data = data and json.dumps(data) or ''

        request = urllib2.Request(self.base + uri)
        request.get_method = lambda: method.upper()
        self.add_headers_to_req(request, *(self.default_headers))
        if isinstance(headers, list):
            self.add_headers_to_req(request, *headers)

        return self.Response(self.opener.open(request, data=data))

    @property
    def base(self):
        return 'http://%s:%d' % (self.host or 'localhost', self.port or 80)

    def open(self, method, uri, data=None, status=200):
        response = self.request(method, uri, data=data)
        response.expect(status)
        return response

    def get(self, uri, data=None, expect=200):
        return self.open('GET', uri, data=data, status=expect)

    def head(self, uri, data=None, expect=200):
        return self.open('HEAD', uri, data=data, status=expect)

    def delete(self, uri, data=None, expect=200):
        return self.open('DELETE', uri, data=data, status=expect)

    def post(self, uri, data, expect=200):
        return self.open('POST', uri, data=data, status=expect)

    def put(self, uri, data, expect=200):
        return self.open('PUT', uri, data=data, status=expect)
