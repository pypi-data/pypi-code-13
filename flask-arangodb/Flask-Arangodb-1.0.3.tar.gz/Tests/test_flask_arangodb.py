#!/usr/bin/env python3
# coding=utf-8
import unittest

from flask import Flask

from flask_arangodb.arangodb import ArangoDB


class FlaskRequestTests(unittest.TestCase):
    def setUp(self):
        self.app = Flask('test')
        self.context = self.app.test_request_context('/')
        self.context.push()

    def tearDown(self):
        self.context.pop()


class FlaskArangoDBConfigTests(FlaskRequestTests):
    def setUp(self):
        super(FlaskArangoDBConfigTests, self).setUp()
        self.app.config['ARANGO_SETTINGS'] = {'host': 'localhost', 'port': 8529}
        self.app.config['ARANGO_DB'] = 'flask_arangodb_test'

    def test_direct_initialization(self):
        arango = ArangoDB(self.app)
        self.assertIsNotNone(arango.client)

    def test_init_app(self):
        arango = ArangoDB()
        arango.init_app(self.app)
        self.assertIsNotNone(arango.client)


class FlaskArangoDatabaseTests(FlaskRequestTests):
    def setUp(self):
        super(FlaskArangoDatabaseTests, self).setUp()
        self.app.config['ARANGO_SETTINGS'] = {'host': 'localhost', 'port': 8529}
        self.app.config['ARANGO_DB'] = 'flask_arangodb_test'
        self.arango = ArangoDB()
        self.arango.init_app(self.app)
        if 'flask_arangodb_test' not in self.arango.client.databases():
            self.arango.client.create_database('flask_arangodb_test')

    def test_database_access(self):
        self.assertIsNotNone(self.arango.db.properties())
