from __future__ import unicode_literals

from django import template
from django.utils.safestring import mark_safe

from ..models import SeoMeow

register = template.Library()


@register.simple_tag(takes_context=True)
def put_seo_meow_tags_here(context):
    path = context['request'].path

    try:
        seo_meow = SeoMeow.objects.get(url__iexact=path)
    except SeoMeow.DoesNotExist:
        seo_meow = SeoMeow.objects.get_or_create(url='/')[0]

    result = ('<meta name="description" content="%s">' \
        + '\n\t' + '<meta name="keywords" content="%s">') \
            % (seo_meow.description, seo_meow.keywords)

    return mark_safe(result)
