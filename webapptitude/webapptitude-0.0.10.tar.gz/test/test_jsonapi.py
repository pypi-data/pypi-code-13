from webapptitude import testkit as helper
from webapptitude import WSGIApplication
from webapptitude.jsonapi import JSONRequestHandler, api

from google.appengine.ext import ndb

class TestModel(ndb.Model):
    name = ndb.StringProperty(required=True)


class WriteOnceModel(ndb.Model):
    value = ndb.StringProperty(required=True)


class JSONAPITestSuite(helper.ServiceRequestCase):

    @classmethod
    def getHandlers(cls):
        app = WSGIApplication(config=helper.site_config, debug=True)

        item = TestModel(name='this is a test', id='pizza').put()
        cls.logger.info('Model instance key %r' % item.urlsafe())

        @app.route('/test/one')
        class One(JSONRequestHandler):
            def get(self):
                seven = self.fetch_param('seven', int, default=None)
                self.response.write_json({'result': ((int(seven) + 2) == 9)})

        @app.route('/test/two')
        class Two(JSONRequestHandler):
            def post(self):
                toppings = self.fetch_param('toppings', '^(pepperoni|bacon)$')
                self.response.write_json({'topping': toppings.split(', ')})

        handler = api(TestModel)
        handler.register_routes(app)

        class WriteOnceHandler(api(WriteOnceModel)):

            def is_authorized(self, method=None, model=None, instance=None):
                return (method not in ('delete', 'DELETE'))

        WriteOnceHandler.register_routes(app)

        return app

    headers_json = [('Content-Type', 'application/json')]

    @helper.debug_on()
    def testParameterMatchType(self):
        response = self.testapp.get('/test/one?seven=7',
                                    headers=self.headers_json)
        self.assertTrue(response.json.get('result'))

    def testNegativeMatchString(self):
        param = {'toppings': 'mushroom'}  # this value will fail to match.
        response = self.testapp.post_json('/test/two', param, status=400)
        self.assertEqual(response.status_code, 400)

    def testPositiveMatchString(self):
        param = {'toppings': 'pepperoni'}  # this value will match.
        response = self.testapp.post_json('/test/two', param, status=200)
        self.assertSequenceEqual(response.json.get('topping'), ['pepperoni'])

    def test0APIModelBasic(self):
        headers = self.headers_json
        response = self.testapp.get('/api/data/i/TestModel/', headers=headers)
        data = response.json
        self.assertIsInstance(data, (list, tuple))
        result = [ r.get('name') for r in data ]
        self.assertSequenceEqual(result, [ "this is a test" ])

    def test0APIQueryProperties(self):
        response = self.testapp.get('/api/data/i/TestModel/',
                                    {'name': 'this is a test'},
                                    headers=self.headers_json)
        self.assertIsInstance(response.json, list)
        self.assertEqual(len(response.json), 1)

        #  self.logger.info(repr(response.json))

    def test1APIModelRequestKeyWithUpdate(self):
        """
        NOTE this modifies a specific data store record.

        It therefore runs _after_ the '_0_' test defined above.
        """
        keystring = ndb.Key('TestModel', 'pizza').urlsafe()
        response = self.testapp.get('/api/data/i/TestModel/%s' % keystring,
                                    headers=self.headers_json)
        data = response.json
        # self.logger.info('Model response %r' % data)
        self.assertEqual(data['name'], 'this is a test')
        self.assertTrue(data['$key'])
        self.assertTrue(data['$url'])

        # Issue an update based on the entity URL
        self.testapp.put_json(data['$url'], {
            'name': 'OMG That was an amazing test!'
        }, status=202)

        # Request the same entity again
        response = self.testapp.get('/api/data/i/TestModel/%s' % keystring,
                                    headers=self.headers_json)

        # Check that the update sticks
        self.assertRegexpMatches(response.json['name'], '^OMG')

    def test1APIModelCreate(self):
        response = self.testapp.post_json('/api/data/i/TestModel/',
                                          {'name': 'test2'},
                                          status=201)

        entity_url = response.headers.get('Location')

        response = self.testapp.head(entity_url,
                                     headers=self.headers_json,
                                     status=200)

        response = self.testapp.get(entity_url, headers=self.headers_json)

        self.assertEqual(response.json.get('name'), 'test2')

        response = self.testapp.delete(entity_url,
                                       headers=self.headers_json,
                                       status=202)

    def test1APIWriteOnce(self):

        response = self.testapp.post_json('/api/data/i/WriteOnceModel/',
                                          {'value': 'do not delete me'},
                                          status=201)

        entity_url = response.headers.get('Location')

        response = self.testapp.delete(entity_url,
                                       headers=self.headers_json,
                                       status=403)  # forbidden

