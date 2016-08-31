from webapptitude import decorator
from webapptitude import testkit as helper

import webapp2
from google.appengine.api import users


class UserEmailValidationTest(helper.ServiceRequestCase):

    @classmethod
    def getHandlers(cls):

        class EmailRequired(webapp2.RequestHandler):

            @decorator.require(decorator.user_domain("test.com", "pizza.com"))
            def get(self):
                self.response.write('Authorized')

        yield '/', EmailRequired

    def testAnonymous(self):
        self.testbed.loginAnonymous()
        self.assertFalse(users.get_current_user())
        response = self.testapp.get('/', expect_errors = True)
        self.assertResponse(response, response_code = 401)

    def testDomainMismatch(self):
        self.testbed.loginUser("test@example.com")
        response = self.testapp.get('/', expect_errors = True)
        self.assertResponse(response, response_code = 403)

    def testDomainMatch(self):
        self.testbed.loginUser("example@test.com")
        response = self.testapp.get('/')
        self.assertResponse(response, response_code = 200)

    @helper.debug_on(helper.webtest.AppError)
    def testAltDomainMatch(self):
        self.testbed.loginUser("pepperoni@pizza.com")
        response = self.testapp.get('/')
        self.assertResponse(response, response_code = 200)


