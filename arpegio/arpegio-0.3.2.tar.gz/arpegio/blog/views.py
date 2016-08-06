"""Views for the blog app."""
from itertools import chain
from django.views.generic.detail import DetailView
from django.views.generic import ListView

from .models import Post


class PostList(ListView):
    """Post list view."""
    model = Post
    context_object_name = 'posts'

    def get_queryset(self):
        return list(chain(self.model.objects.sticky(),
                          self.model.objects.public()
                          ))

    def get_paginate_by(self, queryset):
        number_of_post = super(PostList, self).get_paginate_by(queryset)
        return number_of_post or 5

    def get_template_names(self):
        names = super(PostList, self).get_template_names()
        names.append('arpegio-blog/post_list.html')
        return names


class PostDetail(DetailView):
    """Post detail view."""
    model = Post

    def get_template_names(self):
        names = super(PostDetail, self).get_template_names()
        names.append('arpegio-blog/post_detail.html')
        return names
