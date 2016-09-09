from __future__ import unicode_literals

import re
from contextlib import contextmanager

from django.utils import translation
from django.utils.lru_cache import lru_cache
from django.utils.six import unichr

_original_trans = translation._trans

WORDLIKE_REGEXP = re.compile(r'(\w+)', re.UNICODE | re.IGNORECASE)
FORMATLIKE_REGEXP = re.compile(r'((\{.+?\})|(%[a-z0-9_()]+))', re.IGNORECASE)
FORMAT_MEMO_REGEXP = re.compile(r'\u0001(.+?)\u0002')

CHAFF = [
    '\u2582',
    '\u2583',
    '\u2584',
    '\u2585',
    '\u2586',
    '\u2587',
    '\u2588',
]


def _poison_word(word):
    if '%' in word or '{' in word:
        return word
    n = len(CHAFF)
    return ''.join(CHAFF[ord(c) % n] for c in word)


@lru_cache(maxsize=4096)
def poison_string(string):
    """
    Get a poisoned version of the given string.

    This function tries to retain formattability of
    %s/%()s/{} placeholders.

    :param string: The string to poison.
    :return: A poisoned string.
    """
    format_memo = []

    def _memoize_format(m):
        format_memo.append(m.group(0))
        return '\u0001%s\u0002' % unichr(0xE000 + len(format_memo))

    def _unmemoize_format(m):
        return format_memo[ord(m.group(1)) - 0xE000 - 1]

    string = FORMATLIKE_REGEXP.sub(_memoize_format, string)
    string = WORDLIKE_REGEXP.sub(lambda m: _poison_word(m.group(0)), string)
    if format_memo:
        string = FORMAT_MEMO_REGEXP.sub(_unmemoize_format, string)
    return string


class PoisonTrans(object):
    def __getattr__(self, real_name):
        return getattr(_original_trans, real_name)

    def ugettext(self, message):
        return poison_string(message)

    def gettext(self, message):
        return poison_string(message)

    def ngettext(self, singular, plural, number):
        return poison_string(singular)

    def ungettext(self, singular, plural, number):
        return poison_string(singular)

    def pgettext(self, context, message):
        return poison_string(message)

    def npgettext(self, context, singular, plural, number):
        return poison_string(singular)


def enable():
    """
    Enable the poisoner.
    """
    translation._trans = PoisonTrans()


def disable():
    """
    Disable the poisoner (return to the original `trans` object).
    :return:
    """
    translation._trans = _original_trans


@contextmanager
def override(on=True):
    """
    Context manager to temporarily enable (or disable) the poisoner.

    :param on: Whether to enable (True) or disable (False) the poisoner.
    :type on: bool
    """
    old_trans = translation._trans
    if on:
        enable()
    else:
        disable()
    yield
    translation._trans = old_trans
