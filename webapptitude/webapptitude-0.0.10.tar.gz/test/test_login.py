
from webapptitude import testkit as helper

import webapp2
from google.appengine.api import users

from webapptitude.decorator import require, is_admin, is_loggedin
from webapp2_extras.appengine.users import login_required, admin_required

class UserLoginTest(helper.ServiceRequestCase):

    @classmethod
    def getHandlers(cls):

        class LoginStatusHandler(webapp2.RequestHandler):

            def get(self):
                current = users.get_current_user()
                self.response.write('User: <%s> admin(%s)' % (
                    current.email() if current else '',
                    current and users.is_current_user_admin() or False
                ))



        class LoginStatusAdminRequired(webapp2.RequestHandler):

            @require(is_admin)
            def get(self):
                self.response.write('Authorized')

        class LoginRedirectAdmin(webapp2.RequestHandler):

            @admin_required
            def get(self):
                self.response.write('Authorized')

        yield '/', LoginStatusHandler
        yield '/admin/error', LoginStatusAdminRequired
        yield '/admin/redirect', LoginRedirectAdmin


    def testLoginAnonymous(self):
        self.testbed.loginAnonymous()
        self.assertFalse(users.get_current_user())
        response = self.testapp.get('/')
        self.assertResponse(response, body = 'User: <> admin(False)', response_code = 200)

        response = self.testapp.get('/admin/error', expect_errors = True)
        self.assertResponse(response, response_code = 401)


    def testAdminUser(self):
        self.testbed.loginUser(email='admin@example.com', is_admin=True)
        response = self.testapp.get('/admin/error')
        self.assertResponse(response, response_code=200)

    def testAdminRedirect(self):
        self.assertFalse(users.get_current_user())
        response = self.testapp.get('/admin/redirect')
        self.assertResponse(response, response_code = 302)
