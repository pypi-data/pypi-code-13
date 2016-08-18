# coding=utf-8

import json

import tornado.web
from tornado.httputil import url_concat
from gateguard import Schema, StringField

import monstro.testing

from .api import APIHandler


class APIHandlerTest(monstro.testing.AsyncHTTPTestCase):

    class TestSchema(Schema):

        value = StringField()

    def get_app(self):

        class TestHandler(APIHandler):

            schemas = {
                'PUT': {
                    'body': self.TestSchema
                },
                'DELETE': {
                    'query': self.TestSchema
                }
            }

            @tornado.gen.coroutine
            def get(self):
                self.write({'key': 'value'})

            @tornado.gen.coroutine
            def post(self):
                self.write({'key': 'value'})

            @tornado.gen.coroutine
            def put(self):
                self.write(self.data)

            @tornado.gen.coroutine
            def delete(self):
                self.write(self.query)

        return tornado.web.Application(
            [tornado.web.url(r'/', TestHandler, name='test')]
        )

    def test_get(self):
        response = self.fetch('/')

        self.assertEqual(200, response.code)
        self.assertEqual('{"key": "value"}', response.body.decode('utf-8'))

    def test_unsupported_method(self):
        response = self.fetch('/', method='OPTIONS')

        self.assertEqual(405, response.code)

    def test_post(self):
        response = self.fetch('/', method='POST', body='')
        data = json.loads(response.body.decode('utf-8'))

        self.assertEqual(200, response.code)
        self.assertEqual({'key': 'value'}, data)

    def test_post__wrong_json(self):
        response = self.fetch('/', method='POST', body='a')
        data = json.loads(response.body.decode('utf-8'))

        self.assertEqual(400, response.code)
        self.assertEqual(
            {
                'details': {'request_error': 'Unable to parse JSON'},
                'status': 'error',
                'status_code': 400
            }, data
        )

    def test_put(self):
        payload = {'value': 'test'}
        response = self.fetch('/', method='PUT', body=json.dumps(payload))
        data = json.loads(response.body.decode('utf-8'))

        self.assertEqual(200, response.code)
        self.assertEqual(payload, data)

    def test_put__validation_error(self):
        payload = {}
        response = self.fetch('/', method='PUT', body=json.dumps(payload))
        data = json.loads(response.body.decode('utf-8'))

        self.assertEqual(400, response.code)

        self.assertEqual('error', data['status'])
        self.assertEqual(400, data['status_code'])
        self.assertIn('value', data['details'])

    def test_delete(self):
        payload = {'value': 'test'}
        response = self.fetch(url_concat('/', payload), method='DELETE')
        data = json.loads(response.body.decode('utf-8'))

        self.assertEqual(200, response.code)
        self.assertEqual(payload, data)

    def test_delete__validation_error(self):
        payload = {}
        response = self.fetch(url_concat('/', payload), method='DELETE')
        data = json.loads(response.body.decode('utf-8'))

        self.assertEqual(400, response.code)

        self.assertEqual('error', data['status'])
        self.assertEqual(400, data['status_code'])
        self.assertIn('value', data['details'])
