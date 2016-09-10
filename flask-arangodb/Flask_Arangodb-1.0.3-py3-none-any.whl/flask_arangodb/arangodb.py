#!/usr/bin/env python3
# coding=utf-8
import arango
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
        self.app = app
        app.config.setdefault('ARANGO_SETTINGS', {
            "host": "127.0.0.1",
            "port": 8529,
            "username": "root",
            "password": ""
        })
        app.config.setdefault('ARANGO_DB', "default")

    @property
    def client(self):
        ctx = stack.top
        if ctx is not None:
            if not hasattr(ctx, 'arangoclient'):
                ctx.arangoclient = arango.ArangoClient(**current_app.config['ARANGO_SETTINGS'])
            return ctx.arangoclient

    @property
    def db(self):
        return self.client.db(name=self.app.config['ARANGO_DB'])
