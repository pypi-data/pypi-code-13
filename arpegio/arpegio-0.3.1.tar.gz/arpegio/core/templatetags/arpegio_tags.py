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


ALLOWED_TAGS = 'a|abbr|area|audio|b|bdi|bdo|br|button|canvas|cite|'
ALLOWED_TAGS += 'code|data|datalist|del|dfn|em|embed|i|iframe|img|input|'
ALLOWED_TAGS += 'ins|kbd|label|link|map|mark|math|meter|noscrip|object|'
ALLOWED_TAGS += 'output|picture|progress|q|ruby|s|samp|script|select|small|'
ALLOWED_TAGS += 'span|strong|sub|sup|svg|template|textarea|time|u|var|video|'
ALLOWED_TAGS += 'wbr|text'


@register.filter(is_safe=True)
@stringfilter
def linebreakshtml(text):
    """Acts like the default breaklines but respect html tags."""
    lines = re.split(r'\n{2,}', text.replace('\r', ''))
    lines = [line.strip() for line in lines]
    paragraphs = ['<p>%s</p>' % line.replace('\n', '<br>')
                  if re.match(r'^([\w\d\s]|<(%s)(\s+.*)*>)' % ALLOWED_TAGS, line)
                  else
                  line
                  for line in lines]
    return mark_safe(''.join(paragraphs))
