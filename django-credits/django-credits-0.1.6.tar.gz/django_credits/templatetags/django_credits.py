from django import template
from django.conf import settings

from ..models import Credit


register = template.Library()

DEFAULT_DJANGO_CREDITS_DELAY = 4000  # milliseconds


@register.inclusion_tag("django_credits.html")
def django_credits():
    return {"credits": Credit.objects.all(),
            "django_credits_delay": getattr(settings,
                                            "DJANGO_CREDITS_DELAY",
                                            DEFAULT_DJANGO_CREDITS_DELAY)}
