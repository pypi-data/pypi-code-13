# -*- coding: utf-8 -*-
# @Author: linlin
# @Date:   2016-05-24 16:21:07
# @Last Modified by:   drinks
# @Last Modified time: 2016-05-25 10:30:34
from __future__ import print_function

import os
from random import choice
from traceback import format_exc, print_exc

__all__ = ('colored', 'cprint', 'color_write')
ATTRIBUTES = dict(zip([
    'bold', 'dark', '', 'underline', 'blink', '', 'reverse', 'concealed'
], list(range(1, 9))))
del ATTRIBUTES['']

HIGHLIGHTS = dict(zip([
    'on_grey', 'on_red', 'on_green', 'on_yellow', 'on_blue', 'on_magenta',
    'on_cyan', 'on_white'
], list(range(40, 48))))
COLORS = dict(zip([
    'grey',
    'red',
    'green',
    'yellow',
    'blue',
    'magenta',
    'cyan',
    'white',
], list(range(30, 38))))
COLORS.pop('grey')
RESET = '\033[0m'


def colored(text, color=None, on_color=None, attrs=None):
    if os.getenv('ANSI_COLORS_DISABLED') is None:
        fmt_str = '\033[{0}m{1}'
        text = color is not None and fmt_str.format(COLORS[color],
                                                    text) or text
        text = on_color is not None and fmt_str.format(HIGHLIGHTS[on_color],
                                                       text) or text
        if attrs is not None:
            for attr in attrs:
                text = fmt_str.format(ATTRIBUTES[attr], text)
        text = ''.join([text, RESET])
    return text


def cprint(text, color=None, on_color=None, attrs=None, **kwargs):
    print(colored(text, color=color, on_color=on_color, attrs=attrs), **kwargs)


def color_write(func):
    def warp(text):
        color = choice(list(COLORS))
        text = func(colored(text, color=color))
        return text

    return warp


_ignore = True


def color_exc(exc):
    global _ignore
    origi_errors = format_exc(exc).splitlines()
    errors = map(lambda x: _colored(x), origi_errors)
    errors[-1] = _colored(origi_errors[-1], direct=True)
    errors = '\n'.join(errors)
    return errors


def _colored(error, direct=False):
    global _ignore
    if not _should_ignore(error) or direct:
        return colored(error, 'red', attrs=['bold'])
    return colored(error, 'green', attrs=['bold'])


def _should_ignore(error):
    global _ignore
    if error.strip(' ').startswith('File'):
        _ignore = False
        if any((x in error for x in ('site-packages', 'dist-packages', 'lib'))):
            _ignore = True
    return _ignore
try:
    raise ValueError()
except ValueError as e:
    print(color_exc(e))

