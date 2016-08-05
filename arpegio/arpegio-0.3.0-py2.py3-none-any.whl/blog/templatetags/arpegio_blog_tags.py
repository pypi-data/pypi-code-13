"""Templatetags for the Blog app."""
from django import template

from ..models import Post


register = template.Library()


@register.inclusion_tag('arpegio-blog/tags/recent_posts.html')
def recent_posts(num_post=5):
    """List the recent posts."""
    posts = Post.objects.all()[:num_post]
    return {'posts': posts}
