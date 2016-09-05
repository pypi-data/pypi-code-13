from warnings import warn

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from jinja2.ext import _CommentFinder, extract_from_ast, babel_extract


def django_jinja2_extract(fileobj, keywords, comment_tags, options):
    # Use the Django-Jinja2 -configured Jinja2 environment for extraction.
    # Otherwise mimicked from `jinja2.ext.babel_extract`
    environment = options['environment']

    source = fileobj.read().decode(settings.DEFAULT_CHARSET)
    node = environment.parse(source)
    tokens = list(environment.lex(environment.preprocess(source)))

    finder = _CommentFinder(tokens, comment_tags)
    for lineno, func, message in extract_from_ast(node, keywords):
        yield lineno, func, message, finder.find_comments(lineno)


def jinja2_extract(fileobj, keywords, comment_tags, options):
    """
    Extract messages from Jinja2 files, attempting to use a Django-Jinja2
    :param fileobj:
    :param keywords:
    :param comment_tags:
    :param options:
    :return:
    """
    try:
        from django_jinja.backend import Jinja2
        options = options.copy()
        options['environment'] = Jinja2.get_default().env
        extractor = django_jinja2_extract
    except (ImportError, ImproperlyConfigured) as exc:  # pragma: no cover
        warn('falling back to default jinja2 extractor due to %s' % exc)
        extractor = babel_extract
    return extractor(fileobj, keywords, comment_tags, options)
