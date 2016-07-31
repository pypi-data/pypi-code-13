# coding=utf-8
from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.conf.urls import url

from . import views


if getattr(settings, 'DJANGO_NEWS_ALLOW_CATEGORY_LIST', True):
    urlpatterns = [
        url(r'^$', views.CategoryListView.as_view(),
            name='category_list'),
    ]
else:
    urlpatterns = []


urlpatterns.extend([
    url(r'^(?P<slug>[\w,-]+)/$', views.EntryListView.as_view(),
        name='entry_list'),
    url(r'^(?P<category_slug>[\w,-]+)/(?P<slug>[\w,-]+)/$',
        views.EntryDetailView.as_view(), name='entry_detail'),
])
