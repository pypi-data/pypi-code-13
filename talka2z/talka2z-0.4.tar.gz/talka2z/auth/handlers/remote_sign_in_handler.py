from urllib.parse import urlencode

from tornado.httpclient import AsyncHTTPClient
from tornado.web import RequestHandler
from tornado.web import HTTPError as ServerHTTPError
from tornado.httpclient import HTTPError as ClientHTTPError
from tornado.escape import json_decode
from tornado import gen

from blueshed.micro.web.user_mixin import UserMixin
from blueshed.micro.web.cors_mixin import CorsMixin, cors


class RemoteSignInHandler(UserMixin, CorsMixin, RequestHandler):
    '''
        Validates a one-time-password with an auth server and
        puts the result into our access control cookie
        and redirects.
    '''

    def initialize(self, service_name, service_secret, auth_url, http_origins=None):  # noqa
        self.service_name = service_name
        self.service_secret = service_secret
        self.auth_url = auth_url

        # cors options
        self.set_cors_methods('GET,OPTIONS')
        if http_origins:
            self.set_cors_whitelist(http_origins)

    def write_error(self, *args, **kwargs):
        '''
        Must override base write error to stop uncaught
        HTTP errors from clearing CORS headers
        '''
        self.write_cors_headers()
        RequestHandler.write_error(self, *args, **kwargs)

    def options(self):
        return self.cors_options()

    @property
    def auth_headers(self):
        return {
            "service-name": self.service_name,
            "service-secret": self.service_secret
        }

    @cors
    @gen.coroutine
    def get(self):
        # get otp from request
        otp = self.get_argument("otp")

        try:
            # make request to auth server
            response = yield AsyncHTTPClient().fetch(
                self.auth_url + '/control/get_user',
                method="POST",
                headers=self.auth_headers,
                body=urlencode({"user_otp": otp})
            )
        except ClientHTTPError as error:
            # check content type for json to try and parse result
            if error.response and error.response.headers.get('Content-Type') is 'application/json; charset=UTF-8':
                # decode the response
                content = json_decode(error.response.body)

                # catch client otp errors
                if content['status_code'] == 400:
                    raise ServerHTTPError(401, reason=content['message'])

            # handle all other cases as internal errors
            raise error

        else:
            # set client cookie and respond
            content = json_decode(response.body)
            self.set_secure_cookie(self.cookie_name, str(content['result']['id']))
            self.write({"result": "OK"})
            self.finish()
