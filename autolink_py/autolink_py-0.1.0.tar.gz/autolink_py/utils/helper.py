#!/usr/bin/env python

# standard library imports

# third party related imports
import re
import six

# local library imports


def escape_url(url):

    return url.replace('&', '&amp;')


def force_unicode(s, encoding='utf-8', errors='strict'):

    """
    Similar to smart_text, except that lazy instances are resolved to
    strings, rather than kept as lazy objects.
    """

    # Handle the common case first, saves 30-40% when s is an instance of
    # six.text_type. This function gets called often in that setting.

    if isinstance(s, six.text_type):
        return s

    if not isinstance(s, six.string_types):

        if six.PY3:
            if isinstance(s, bytes):
                s = six.text_type(s, encoding, errors)
            else:
                s = six.text_type(s)
        else:
            s = six.text_type(bytes(s), encoding, errors)

    else:
        
        # Note: We use .decode() here, instead of six.text_type(s,
        # encoding, errors), so that if s is a SafeBytes, it ends up being
        # a SafeText at the end.

        s = s.decode(encoding, errors)
    return s


def re_find(regex, s):

    m = re.search(regex, s)
    if m:
        return m.group()