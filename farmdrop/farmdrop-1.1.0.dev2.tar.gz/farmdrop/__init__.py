from __future__ import absolute_import
__version__ = '1.1.0.dev2'

try:
    from .celery import app as celery_app
except ImportError:
    print('WARN: Celery tasks will not run properly without celery installed')

