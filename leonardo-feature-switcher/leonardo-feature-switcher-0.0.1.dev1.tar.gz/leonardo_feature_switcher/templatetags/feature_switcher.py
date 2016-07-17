
from __future__ import absolute_import, unicode_literals

from django import template
from leonardo_feature_switcher import is_off
from leonardo_feature_switcher import is_on

register = template.Library()


@register.simple_tag(takes_context=True, name="is_on")
def is_on_func(context, action, *args, **kwargs):
    """
    {% is_on "my_feature" %}
    {% if my_feature %}
    {% endif %}
    """
    request = context['request']

    kwargs.update({
        'context': context,
    })

    context[action] = is_on(request, action, **kwargs)

    return ''


@register.simple_tag(takes_context=True, name="is_off")
def is_off_func(context, action, *args, **kwargs):
    """
    {% is_off "my_feature" %}
    {% if my_feature %}
    {% endif %}
    """
    request = context['request']

    kwargs.update({
        'context': context,
    })

    context[action] = is_off(request, action, **kwargs)

    return ''
