from webapptitude import testkit as helper
from webapptitude import WSGIApplication
from webapptitude import RequestHandler
from webapptitude.template import TemplatePartial


class ApplicationTest(helper.ServiceRequestCase):

    @classmethod
    def getHandlers(cls):
        app = WSGIApplication(config=helper.site_config, debug=True)

        @app.route('/test')
        class RequestHandlerTest(RequestHandler):
            def get(self):
                return 'This is a test'

        @app.route('/test/json')
        class JSONResponder(RequestHandler):
            def get(self):
                self.response.write_json({
                    'test': True,
                    'ip_addr': self.request.remote_addr,
                    'hostname': self.request.hostname,
                    'input': dict(self.request.input)
                })

        @app.route('/test/template')
        class TemplateResponder(RequestHandler):
            def get(self):
                title = dict(self.request.input).get('title', 'NO TITLE')
                self.response.cachable(10)
                return self.respond_with_template('example.html', title=title)


        # A handler that serves a partial (component) from a template...
        app.route('/test/partial', TemplatePartial('example.html', 'body'))

        return app


    @helper.debug_on(AssertionError,Exception)
    def testRequestContent(self):
        response = self.testapp.get('/test')
        self.assertEqual(response.body, 'This is a test')

    def testJSONResponse(self):
        response = self.testapp.get('/test/json?data=whatever')
        data = response.json

        self.assertEqual(data['input']['data'], 'whatever')
        self.assertEqual(data['test'], True)

    def testTemplateHandling(self):
        response = self.testapp.get('/test/template?title=test')
        self.assertIn('<title>test</title>', response.body)

    def testTemplatePartial(self):
        response = self.testapp.get('/test/partial')
        self.assertEqual(response.body.strip(), "This is an awesome template. "
                                                "I'd give it 100K thumbs up.")
