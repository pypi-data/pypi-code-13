u'''

Provided C-style string process methods.

@date 2015-03-22
@author Hong-She Liang <starofrainnight@gmail.com>
'''

from __future__ import absolute_import
import six


def escape(text):
    if six.PY2:
        return text.encode(u'unicode-escape').replace(u'"', u'\\"').replace(u"'", u"\\'")
    else:
        return text.encode(u'unicode-escape').decode().replace(u'"', u'\\"').replace(u"'", u"\\'")


def unescape(text):
    return six.b(text).decode(u'unicode-escape')
