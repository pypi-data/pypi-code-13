from restify import *
from restify.dsn import *
from restify.routing import *
from restify.util import *

import subprocess

__git_label__ = ''
try:
    __git_label__ = subprocess.check_output(
        [
            'git',
            'rev-parse',
            '--short',
            'HEAD'
        ])
except subprocess.CalledProcessError:
    __git_label__ = 'RELEASE'

__version__ = '0.0.2-5'
__release__ = '{}-{}'.format(__version__, __git_label__).strip()

__description__ = """ restify is a small library that tries to make it easier
to write and maintain a small REST API system which runs on top of Bottle.
"""
