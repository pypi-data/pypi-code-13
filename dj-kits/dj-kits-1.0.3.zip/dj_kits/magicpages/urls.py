# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import patterns, url

urlpatterns = []

def magic_page_urlpatterns():
    return patterns(
        '',
        url(r'^(?P<path>.*)$', 'dj_kits.magicpages.views.magic_page')
    )

# Only append if urlpatterns are empty
if settings.DEBUG and not urlpatterns:
    urlpatterns += magic_page_urlpatterns()
