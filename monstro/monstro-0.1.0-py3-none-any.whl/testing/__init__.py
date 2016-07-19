# coding=utf-8

import tornado.gen
import tornado.testing
import tornado.ioloop

from monstro.conf import settings
import monstro.orm.db


class AsyncTestCase(tornado.testing.AsyncTestCase):

    def get_new_ioloop(self):
        return tornado.ioloop.IOLoop.current()

    def setUp(self):
        super().setUp()

        settings.mongodb_database = (
            settings.mongodb_database.rstrip('__test__') + '__test__'
        )
        self.connection = monstro.orm.db.get_motor_connection(
            io_loop=self.io_loop
        )

        self.setUpHelper()

    def tearDown(self):
        self.tearDownHelper()
        super().tearDown()

    @tornado.gen.coroutine
    def setUpHelper(self):
        pass

    @tornado.gen.coroutine
    def tearDownHelper(self):
        yield self.connection.drop_database(settings.mongodb_database)


class AsyncHTTPTestCase(tornado.testing.AsyncHTTPTestCase):

    def get_new_ioloop(self):
        return tornado.ioloop.IOLoop.current()

    def setUp(self):
        super().setUp()

        settings.mongodb_database = (
            settings.mongodb_database.rstrip('__test__') + '__test__'
        )
        self.connection = monstro.orm.db.get_motor_connection(
            io_loop=self.io_loop
        )

        self.setUpHelper()

    def tearDown(self):
        self.tearDownHelper()
        super().tearDown()

    @tornado.gen.coroutine
    def setUpHelper(self):
        pass

    @tornado.gen.coroutine
    def tearDownHelper(self):
        yield self.connection.drop_database(settings.mongodb_database)
