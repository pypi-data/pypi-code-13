# -*- coding: utf-8 -*-

"""
Utilities for converting from GitHub markdown to Confluence wiki content.
"""

from __future__ import print_function
from __future__ import unicode_literals

import base64
import markdown
import re


class ConfluenceLinkExtension(markdown.extensions.Extension):
    """Defines a Markdown library extension which will convert [[Page Title]] to a wiki link.
    """

    pattern = r'\[\[((?P<linktext>[^|]+)\|)?(?P<pagetitle>[\w0-9_ -]+)\]\]'

    def __init__(self, *args, **kwargs):
        super(ConfluenceLinkExtension, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md, md_globals):
        md.inlinePatterns.add('confluencelink', ConfluenceLink(self.pattern), '<not_strong')


class ConfluenceLink(markdown.inlinepatterns.Pattern):
    """Defines a pattern for recognizing a wiki link that needs to be converted to Confluence.
    """

    def handleMatch(self, match):
        title = match.groupdict()['pagetitle'].replace('"', '&quot;')
        if not title.strip():
            return ''

        link = markdown.util.etree.Element('ac:link')
        link_ri_page = markdown.util.etree.SubElement(link, 'ri:page')
        link_ri_page.set('ri:content-title', title)
        link_text = match.groupdict().get('linktext')
        if link_text:
            link_text_b64 = base64.encodestring(link_text.encode('utf-8')).strip()
            link_body = markdown.util.etree.SubElement(link, 'ac:plain-text-link-body')
            link_body.text = '[base64-cdata[{}]]'.format(link_text_b64.decode('ascii'))
        return link


def remove_first_h1_underlined(text):
    r"""
    Removes the first top-level header from a Markdown text block if it uses underlines.

    >>> remove_first_h1_underlined('Three equals\n===\n\n\n\nHello!\n\nGoodbye!\n')
    'Hello!\n\nGoodbye!\n'

    >>> remove_first_h1_underlined('Way more equal signs\n===================\n\n\n\nHello!\n\nGoodbye!\n')
    'Hello!\n\nGoodbye!\n'

    >>> remove_first_h1_underlined('Two equals does not cut it\n==\n\n\n\nHello!\n')
    'Two equals does not cut it\n==\n\n\n\nHello!\n'

    >>> remove_first_h1_underlined('Dashes do not count\n---------\n\n\n\nHello!\n\nGoodbye!\n')
    'Dashes do not count\n---------\n\n\n\nHello!\n\nGoodbye!\n'

    >>> remove_first_h1_underlined('\n\nRemove first\n===\n\nDo not remove second\n===\n\n')
    'Do not remove second\n===\n\n'
    """
    return re.sub(r'^(\r?\n)*.+\r?\n===+(\r?\n)+', '', text)


def remove_first_h1_hashtags(text):
    r"""
    Removes the first top-level header from a Markdown text block if it uses hashtags:

    >>> remove_first_h1_hashtags('# Remove this one\n\n# Not this one\n\nHello!\n')
    '# Not this one\n\nHello!\n'
    """
    return re.sub(r'^(\r?\n)*# .+(\r?\n)+', '', text)


def remove_first_h1(text):
    return remove_first_h1_underlined(remove_first_h1_hashtags(text))


def remove_comments(text):
    r"""
    Removes Markdown comments from the given text body.

    >>> remove_comments(
    ...     'This line will be fine.\n'
    ...     'This line will also be fine.\n'
    ...     '\n'
    ...     '[//]: # This line is a comment.\n'
    ...     'This is the last line.\n'
    ... )
    'This line will be fine.\nThis line will also be fine.\n\nThis is the last line.\n'

    >>> remove_comments(
    ...     '[//]: # This line is a comment.\n'
    ...     'However, [//]: # this line stays.\n'
    ... )
    'However, [//]: # this line stays.\n'
    """
    return re.sub(r'(^|\n)\[//\]: #.*(\n|$)', r'\1', text)


def fix_cdata(text):
    """
    ElementTree does not support CDATA, so we do some postprocessing to the output
    of the Markdown library.
    """
    expr = r'\[base64-cdata\[([A-Za-z0-9\+\/]+)\]\]'

    def repl(match):
        link_text_b64 = match.groups()[0]
        link_text = base64.decodestring(link_text_b64.encode('ascii'))
        # We encoded this string as UTF-8 before putting it into base64 (above)
        return '<![CDATA[{}]]>'.format(link_text.decode('utf-8'))

    return re.sub(expr, repl, text)


def markdown_to_confluence_with_macro(text):
    text = remove_first_h1(text)
    text = remove_comments(text)
    return '''\
        <ac:structured-macro ac:name="markdown" ac:schema-version="1">
            <ac:parameter ac:name="atlassian-macro-output-type">INLINE</ac:parameter>
            <ac:plain-text-body><![CDATA[{}]]></ac:plain-text-body>
        </ac:structured-macro>
        '''.format(text)


def markdown_to_confluence(text):
    text = remove_first_h1(text)
    text = remove_comments(text)
    text = markdown.markdown(text, extensions=[ConfluenceLinkExtension()])
    text = fix_cdata(text)
    return text
