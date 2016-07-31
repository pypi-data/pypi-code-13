# coding=utf-8
from __future__ import absolute_import, unicode_literals

from django import template

from ..models import Category

register = template.Library()


@register.simple_tag(takes_context=True)
def get_active_categories(context):
    """Get a list all active news categories"""
    if 'category_list' in context and len(context['category_list']):
        if isinstance(context['category_list'][0], Category):
            return context['category_list']
    return Category.objects.get_active()
