# -*- coding: utf-8 -*-

import os
import logging
import logging.handlers


def get_log():
    if os.uname()[0] == 'Darwin':
        return '/var/run/syslog'
    elif os.uname()[0] == 'Linux':
        return '/dev/log'
    else:
        return None


def logging_init(verbose_console=False):
    logging.getLogger().setLevel(logging.NOTSET)

    sh = logging.handlers.SysLogHandler(address=get_log())
    sh.setLevel(level=logging.DEBUG)
    sh.setFormatter(
        logging.Formatter('node_maker[%(process)d]: %(levelname)s %(message)s'))
    logging.getLogger().addHandler(sh)

    if verbose_console:
        ch = logging.StreamHandler()
        ch.setLevel(level=logging.DEBUG)
        ch.setFormatter(logging.Formatter(
            '%(asctime)s : %(name)s[%(lineno)d] : %(levelname)s : %(message)s'
        ))
        logging.getLogger().addHandler(ch)
