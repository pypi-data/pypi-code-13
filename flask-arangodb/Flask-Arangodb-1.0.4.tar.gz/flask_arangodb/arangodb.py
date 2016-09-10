#!/usr/bin/env python3
# coding=utf-8
from arango import ArangoClient
from flask import current_app

try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack


class ArangoDB(object):
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.config.setdefault('ARANGO_CLIENT', {"host": "127.0.0.1",
                                                "port": 8529,
                                                "username": "root",
                                                "password": ""})
        app.config.setdefault('ARANGO_DB', {'name': 'default',
                                            'user': None,
                                            'password': None})

    def connect(self):
        return ArangoClient(**current_app.config['ARANGO_CLIENT'])

    @property
    def client(self):
        ctx = stack.top
        if ctx is not None:
            if not hasattr(ctx, 'arango_client'):
                ctx.arango_client = self.connect()
            return ctx.arango_client

    @property
    def db(self):
        if self.client:
            if isinstance(current_app.config['ARANGO_DB'], dict):
                return self.client.db(**current_app.config['ARANGO_DB'])
            else:
                return self.client.db(name=current_app.config['ARANGO_DB'])
