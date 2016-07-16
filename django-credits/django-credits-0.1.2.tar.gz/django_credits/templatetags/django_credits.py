from django import template

from ..models import Credit

register = template.Library()


@register.inclusion_tag("django_credits.html")
def django_credits():
    return {"credits": Credit.objects.all()}
