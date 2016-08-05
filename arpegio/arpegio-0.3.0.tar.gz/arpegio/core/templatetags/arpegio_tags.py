"""Arpegio's templatetags."""
import re

from django import template
from django.utils.safestring import mark_safe
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


@register.filter(is_safe=True)
@stringfilter
def linebreakshtml(text):
    """Acts like the default breaklines but respect html tags."""
    lines = re.split(r'\n{2,}', text.replace('\r', ''))
    lines = [line.strip() for line in lines]
    paragraphs = [line if re.match(r'^<\w+.*>', line) else
                  '<p>%s</p>' % line.replace('\n', '<br>')
                  for line in lines]
    return mark_safe(''.join(paragraphs))
