import logging

import functools
from django.conf import settings

logger = logging.getLogger(__name__)

replace_pairs = getattr(settings, 'REWRITEBODY_PAIRS', [])


def do_replace(content, before_after):
    before, after = before_after
    return content.replace(before, after)


def update_response_content(response, attribute_name):
    content = getattr(response, attribute_name)
    functools.reduce(do_replace, replace_pairs, content)
    setattr(response, attribute_name, content)


class RwriteBodyMiddleware(object):
    def process_response(self, request, response):
        if response.has_header('Content-Type') and 'text/html' in response['Content-Type']:
            if hasattr(response, 'streaming_cnootent'):
                update_response_content(response=response, attribute_name='streaming_content')
            elif hasattr(response, 'content'):
                update_response_content(response=response, attribute_name='content')
            else:
                logger.debug('`%s` has no attribute `streaming_content` and `content`. Ignored')
        return response
