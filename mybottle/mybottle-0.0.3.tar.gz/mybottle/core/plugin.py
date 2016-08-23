# -*- coding:utf-8 -*-
import logging
from datetime import datetime
from functools import wraps

from bottle import request, response

from mybottle.core.app_common import app


def add_db_close_plugin(db_instance_list):
    def db_close(callback):
        def wrapper(*args, **kwargs):
            body = callback(*args, **kwargs)
            for db_instance in db_instance_list:
                db_instance.close()
            return body

        return wrapper

    app.install(db_close)


def log_to_logger(fn):
    """
    Wrap a Bottle request so that a log line is emitted after it's handled.
    (This decorator can be extended to take the desired logger as a param.)
    """

    @wraps(fn)
    def _log_to_logger(*args, **kwargs):
        request_time = datetime.now()
        actual_response = fn(*args, **kwargs)
        # modify this to log exactly what you need:
        logging.info('%s %s %s %s %s' % (request.remote_addr,
                                         request_time,
                                         request.method,
                                         request.url,
                                         response.status))
        return actual_response

    return _log_to_logger
