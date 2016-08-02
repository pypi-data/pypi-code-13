# coding=utf-8

import tornado.web
import tornado.gen


class RequestHandler(tornado.web.RequestHandler):

    @tornado.gen.coroutine
    def prepare(self):
        self.set_header('Server', '')
