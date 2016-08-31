"""Test kit for the request handlers' decorators, etc"""

from webapptitude import testkit as helper
from webapptitude import WSGIApplication
from webapptitude import RequestHandler
from webapptitude import decorator

import re

class DecoratorTest(helper.ServiceRequestCase):

    @classmethod
    def getHandlers(cls):


        app = WSGIApplication(debug=True, config=helper.site_config)

        @app.route('/header/match')
        class MatchHandler(RequestHandler):

            @decorator.require(decorator.match_header('X-Header-Test', "^valid$"))
            def get(self):
                return self.response.write("OK")

        @app.route('/')
        class Default(RequestHandler):
            def get(self):
                return self.response.write("Hi there.")



        return app

    def testPlainRequest(self):
        response = self.testapp.get('/')
        self.assertEqual(response.body, "Hi there.")


    def testRequestHeaderValid(self):
        headers = [('X-Header-Test', 'valid')]
        response = self.testapp.get('/header/match', None, headers)
        self.assertEqual(response.body, "OK")


    def testRequestHeaderInvalid(self):
        response = self.testapp.get('/header/match', status=400)
        self.assertNotEqual(response.body, "OK")