"""Arpegio's templatetags."""
import re

from django import template
from django.template.defaultfilters import stringfilter


register = template.Library()


@register.filter()
@stringfilter
def more(text, url='#'):
    """Adds a 'Read more' tag to the text."""
    value = re.split(r'<!--\s*more\s*-->', text)
    more_tag = '<p><a href="%s" class="more-link">Read More</a></p>'
    more_link = more_tag % url
    if len(value) > 1:
        text = '%s%s' % (value[0], more_link)
    return text
