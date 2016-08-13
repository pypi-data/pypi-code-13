#!/usr/bin/env python
# coding: utf8

import os

import tornado.ioloop
import tornado.web
from tornado.options import options, define
from xtls.logger import get_logger

logger = get_logger(__file__)

define('host', '0.0.0.0', basestring, 'host')
define('port', 9999, int, 'port')


def make_app():
    from apps.urls import handlers
    import apps.uimodules

    base_path = os.path.dirname(os.path.dirname(__file__))

    settings = {
        'xsrf_cookies': True,
        'cookie_secret': 'qergq342&%^%$#@!ERQF2g45yhq3w',
        'template_path': os.path.join(base_path, 'templates/default'),
        'static_path': os.path.join(base_path, 'static/default'),
        'ui_modules': apps.uimodules,
        'login_url': "/login",
        'debug': True
    }
    app = tornado.web.Application(handlers, **settings)
    return app


def main():
    app = make_app()
    app.listen(options.port, options.host)
    logger.info('xmemx server run at http://{host}:{port}'.format(host=options.host, port=options.port))
    tornado.ioloop.IOLoop.current().start()
