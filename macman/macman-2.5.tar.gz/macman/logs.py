#!/usr/bin/python
# Filename: logs.py

import logging
from logging.handlers import RotatingFileHandler
import os
import __builtin__


def setupLogging(log_file=None):
    """  Setup logging parameters. Log files are stored in the '/usr/local/techops/logs' directory

    If no log_file provided, logging will not occur

    Example:
        setLogging('SetDock.log')

    """

    # if no log file name provided, don't setup logging
    if log_file is None:
        __builtin__.log = None

    # if log file name provided, setup logging
    else:

        # set directory path for log storage and create if it doesn't exist
        log_path = '/usr/local/techops/logs/'
        if not os.path.exists(log_path):
            os.makedirs(log_path)

        # setup log rotation
        # mode = append, max file size = 5mb, retain one copy
        handler = RotatingFileHandler('%s%s' % (log_path, log_file), mode='a', maxBytes=5 * 1024 * 1024, backupCount=1,
                                      encoding=None, delay=0)

        # set log format
        log_formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        handler.setFormatter(log_formatter)

        handler.setLevel(logging.INFO)

        log = logging.getLogger('root')
        log.setLevel(logging.INFO)
        log.addHandler(handler)

        # pass log to __builtin__ so it will be accessible across the module
        __builtin__.log = log


def writeLog(log_string=None):
    """ If setLogging has been called and a log_file specified, write to log.

    If log_string contains \\n, insert \\t before for formatting. This formatting helps keep the log files neat
    and individual entries seperate.

    Example:
        writeLog('Write this to a log')

    """

    if log and log_string:
        log_string = '\t'.join(log_string.strip().splitlines(True))
        log.info(log_string)
