# coding=utf-8

import sys
import argparse
import logging

import tornado.ioloop
import tornado.httpserver

from monstro.core.app import application


logger = logging.getLogger('tornado.general')
logger.setLevel(logging.INFO)


def execute():
    argparser = argparse.ArgumentParser(description='Run Monstro server')

    argparser.add_argument('--host', default='127.0.0.1')
    argparser.add_argument('--port', default=8000)

    args = argparser.parse_args(sys.argv[2:])

    server = tornado.httpserver.HTTPServer(application)
    server.bind(address=args.host, port=args.port)

    logger.info('Listen on {0.host}:{0.port}'.format(args))

    try:
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        tornado.ioloop.IOLoop.instance().stop()
