from tornado.web import RequestHandler

from blueshed.micro.web.user_mixin import UserMixin
from blueshed.micro.web.cors_mixin import CorsMixin, cors


class RemoteSignOutHandler(UserMixin, CorsMixin, RequestHandler):
    ''' Removes the cookie from application settings. '''

    def initialize(self, http_origins=None):
        self.set_cors_methods('GET,OPTIONS')

        if http_origins:
            self.set_cors_whitelist(http_origins)

    def options(self):
        return self.cors_options()

    @cors
    def get(self):
        ''' removes cookie and responds to confirm '''
        self.clear_cookie(self.cookie_name)
        self.write({"result": "OK"})
