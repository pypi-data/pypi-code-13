# -*- coding: utf-8 -*-

import logging


logger = logging.getLogger(__file__)


def check_options(**kwargs):
    if 'make' in kwargs:
        opts = kwargs.get('make')
        arg = [['node_name', True], ['game', True], ['slots', True],
               ['token', False, ['cs_go', 'tf2']]]

        for item in arg:
            if not opts.get(item[0], False):
                if item[1]:
                    return False
                else:
                    if opts['game'] in item[2]:
                        return False

        return True

    elif 'restart' in kwargs:
        arg = [['node_name', True]]
        for item in arg:
            if not kwargs['restart'].get(item[0], False):
                if item[1]:
                    return False
        return True

    elif 'stop' in kwargs:
        arg = [['node_name', True]]
        for item in arg:
            if not kwargs['stop'].get(item[0], False):
                if item[1]:
                    return False
        return True

    elif 'start' in kwargs:
        arg = [['node_name', True]]
        for item in arg:
            if not kwargs['start'].get(item[0], False):
                if item[1]:
                    return False
        return True

    elif 'remove' in kwargs:
        arg = [['node_name', True]]
        for item in arg:
            if not kwargs['remove'].get(item[0], False):
                if item[1]:
                    return False
        return True

    else:
        return False
