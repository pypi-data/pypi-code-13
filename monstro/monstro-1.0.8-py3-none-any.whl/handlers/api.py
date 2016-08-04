# coding=utf-8

import json

import tornado.web
import tornado.gen

from .base import RequestHandler


class APIHandler(RequestHandler):

    schemas = {}

    def initialize(self):
        self.data = {}
        self.query = {}

    def write_error(self, status_code, details=None, **kwargs):
        return self.write({
            'status': 'error',
            'status_code': status_code,
            'details': details
        })

    def get_query_schema(self):
        return self.schemas.get(self.request.method, {}).get('query')

    def get_body_schema(self):
        return self.schemas.get(self.request.method, {}).get('body')

    @tornado.gen.coroutine
    def prepare(self):
        yield super().prepare()

        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Content-Type', 'application/json')

        if self.request.body:
            try:
                self.data = json.loads(self.request.body.decode('utf-8'))
            except (ValueError, UnicodeDecodeError, TypeError):
                self.send_error(
                    400, details={'request_error': 'Unable to parse JSON'}
                )

            schema = self.get_body_schema()

            if schema:
                try:
                    self.data = schema.validate(self.data)
                except schema.ValidationError as e:
                    self.send_error(400, details=e.error)

        self.query = {}
        for key, value in self.request.query_arguments.items():
            self.query[key] = value[0].decode('utf-8')

        schema = self.get_query_schema()

        if schema:
            try:
                self.query = schema.validate(self.query)
            except schema.ValidationError as e:
                self.send_error(400, details=e.error)
