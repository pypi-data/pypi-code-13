"""Urls for the blog app."""
from django.conf.urls import url

from .views import PostDetail, PostList


app_name = 'blog'  # pylint: disable=invalid-name

urlpatterns = [
    url(r'^$',
        PostList.as_view(),
        name='blog',
        ),
    url(r'page/(?P<page>[\d])/$',
        PostList.as_view(),
        name='blog',
        ),
    url(r'^post/(?P<slug>[\w\d-]+)/$',
        PostDetail.as_view(),
        name='post'
        ),
]
