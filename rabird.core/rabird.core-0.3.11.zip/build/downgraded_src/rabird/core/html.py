# -*- coding: utf-8 -*-


u'''
@date 2014-4-14

Some helpful utilities use with html.

@author Hong-She Liang <starofrainnight@gmail.com>
'''

from __future__ import absolute_import
from six.moves import html_entities
from six.moves import html_parser
import six
import xml.sax.saxutils

# escape() and unescape() takes care of &, < and >.
html_escape_table = {
    u'"': u"&quot;",
    u"'": u"&apos;",
    u'\r\n': u"<BR />",
    u'\r': u"<BR />",
    u'\n': u"<BR />",
    u' ': u"&nbsp;",
}
html_unescape_table = dict((v, k) for k, v in list(html_escape_table.items()))
for k, v in list(html_entities.codepoint2name.items()):
    html_unescape_table[u'&%s;' % (v)] = unichr(k)


def escape(text):
    return xml.sax.saxutils.escape(text)


def unescape(text):
    return xml.sax.saxutils.unescape(text)


def display_escape(text):
    return xml.sax.saxutils.escape(text, html_escape_table)


def display_unescape(text):
    output_text = u''

    i = 0
    while(i < len(text)):
        try:
            skip_len = 0
            for k, v in list(html_unescape_table.items()):
                if text[i:i + len(k)] == k:
                    skip_len = len(k) - 1
                    output_text += v
                    break

            if skip_len <= 0:
                output_text += text[i]

            i += skip_len
        finally:
            i += 1

    return xml.sax.saxutils.unescape(output_text)
