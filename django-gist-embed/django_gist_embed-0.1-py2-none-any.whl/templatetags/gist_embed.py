from django import template
from django.utils.html import format_html
register = template.Library()

@register.simple_tag
def gist(id, *args, **kwargs):
    hide_numbers = kwargs.get('hide_numbers')
    hide_footer = kwargs.get('hide_footer')
    gist_file = kwargs.get('gist_file')
    gist_line = kwargs.get('gist_line')
    hide_loading = kwargs.get('hide_loading')

    attributes = {}
    if hide_numbers:
        attributes['data-gist-hide-line-numbers'] = "true"
    if hide_footer:
        attributes['data-gist-hide-footer'] = "true"
    if hide_loading:
        attributes['data-gist-show-loading'] = "false"
    if gist_file:
        attributes['data-gist-file'] = gist_file
    if gist_line:
        attributes['data-gist-line'] = gist_line

    attribute_str = ""
    for key in attributes:
        attribute_str += key + "=\"" + attributes.get(key) + "\" "

    return format_html('<code data-gist-id="%s" %s></code>' % (id, attribute_str))
