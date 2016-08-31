"""
Import the core components of standard applications.
"""
import os
# import sys

from util import is_dev_server, is_prod_server

from test import fix_appengine_sys_path
from version import __version__  # noqa

if not (is_prod_server() or is_dev_server()):
    fix_appengine_sys_path(noisy=False)

from webapp2 import exc as exceptions  # noqa
from application import WSGIApplication  # noqa
from handlers import RequestHandler  # noqa
