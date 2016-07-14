#!/usr/bin/env python

# standard library imports
import re

# third party related imports

# local library imports
from autolink_py.component import Mail, Url
from autolink_py.values.replace_type import ReplaceType
from autolink_py.utils.helper import (
    escape_url,
    force_unicode,
    re_find
)
from autolink_py.values import (
    combined_re,
    proto_re,
    punct_re
)


class AutoLinker(object):

    def __init__(self):

        self.replaced_type = None

    def linkify(self, text, replaced_type=None):

        """
        Convert URL-like and email-like strings into links.
        """

        self.replaced_type = replaced_type

        # Make replaces
        return re.sub(combined_re, self._repl, force_unicode(text))

    def _repl(self, match):

        """
        Currently, the replace_type can be 'HTML' or 'MARKDOWN', if you
        want to replace url with other format, you can inherit class
        AutoLinker and implement link_repl to customize.
        """

        matches = match.groupdict()
        if matches['url']:
            instance = Url(matches['url'])
        else:
            instance = Mail(matches['email'])

        opening, url, closing = self.separate_parentheses(instance.url)
        punct = re_find(punct_re, url)

        if punct:
            url = url[:-len(punct)]

        if re.search(proto_re, url):
            url = url
        else:
            url = instance.proto + url

        if self.replaced_type == ReplaceType.HTML:
            replaced_url = self.replace_url(url)

        elif self.replaced_type == ReplaceType.MARKDOWN:
            replaced_url = self.replace_url(url)

        else:
            replaced_url = self.replace_url(url)

        repl = u'{0!s}{1!s}{2!s}{3!s}'
        return repl.format(opening, replaced_url, punct, closing)

    def separate_parentheses(self, s):
        start = re_find(r'^\(*', s)
        end = re_find(r'\)*$', s)
        n = min(len(start), len(end))
        if n:
            return s[:n], s[n:-n], s[-n:]
        else:
            return '', s, ''

    def replace_url(self, url):

        """
        replace url into customize format. If you want to customize new format
        for the url, you need to create a new class inherit AutoLinker and
        rewrite replace_url function
        """

        if self.replaced_type == ReplaceType.HTML:

            href = escape_url(url)
            return u'<a href="{0!}">{1}</a>'.format(href, url)

        elif self.replaced_type == ReplaceType.MARKDOWN:

            return u'[{0}]({0})'.format(url)

        else:
            raise NotImplementedError
