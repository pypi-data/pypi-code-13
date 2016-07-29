"""Views for the blog app."""
from django.views.generic.detail import DetailView
from django.views.generic import ListView

from .models import Post


class PostList(ListView):
    """Post list view."""
    model = Post
    context_object_name = 'posts'

    def get_paginate_by(self, queryset):
        number_of_post = super(PostList, self).get_paginate_by(queryset)
        return number_of_post or 5


class PostDetail(DetailView):
    """Post detail view."""
    model = Post
