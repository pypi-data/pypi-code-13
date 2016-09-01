# -*- coding:utf-8 -*-
from __future__ import absolute_import, unicode_literals, print_function
import logging
from os.path import abspath, dirname, join, expanduser

PID_FILE = expanduser(u'~/hookman.pid')
BASE_PID_FILE = expanduser(u'~/hookman.pid')
ERROR_LOG = expanduser(u'~/hookman.log')
PROJECT_DIR = u'.'
LOG_LEVER = logging.DEBUG
BASE_PROJECT_DIR = dirname(abspath(__file__))
WEB_LISTENER_PATH = join(BASE_PROJECT_DIR, 'webs', 'weblistener.py')
