#
# Copyright (c) 2016, Michael Conroy
#


import contextlib


from logger import SimpleLogger


__all__ = (
    'SimpleLogger',
    'logger_context',
    'logger_main',
)


@contextlib.contextmanager
def logger_context():
    logging_instance = SimpleLogger()
    yield logging_instance
    logging_instance.clear()


logger_main = SimpleLogger()
