# -*- coding: utf-8 -*-
import re
from urllib import urlencode
from urlparse import urlparse, parse_qsl, urlunparse
from unidecode import unidecode
try:
    from mezzanine.utils.urls import slugify_unicode
except ImportError:
    def slugify_unicode(s):
        return s


_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')


def slugify(text, delim=u'-'):
    """Generates an ASCII-only slug."""
    result = []
    for word in _punct_re.split(text.lower()):
        result.extend(unidecode(word).split())
    return slugify_unicode(unicode(delim.join(result)))


def add_query_params(url, params):
    """
    Inject additional query parameters into an existing URL. If
    parameters already exist with the same name, they will be
    overwritten. Return the modified URL as a string.
    """
    # Ignore additional parameters with empty values
    params = dict([(k, v) for k, v in params.items() if v])
    parts = list(urlparse(url))
    query = dict(parse_qsl(parts[4]))
    query.update(params)
    parts[4] = urlencode(query)
    return urlunparse(parts)
