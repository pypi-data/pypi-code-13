# coding=utf-8

import sys
import argparse

import tornado.ioloop
import tornado.httpserver

from monstro.core.app import application


def execute():
    argparser = argparse.ArgumentParser(description='Run Monstro server')

    argparser.add_argument('port', nargs='?', default=8000)

    args = argparser.parse_args(sys.argv[2:])

    server = tornado.httpserver.HTTPServer(application)
    server.listen(args.port)

    print('Listen on http://127.0.0.1:{}'.format(args.port))

    tornado.ioloop.IOLoop.instance().start()
