# coding=utf-8
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url, include

urlpatterns = [
    url(r'^', include('django_news.urls', namespace='django_news',
                      app_name='django_news')),
]
