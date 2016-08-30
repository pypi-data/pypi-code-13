# -*- coding:utf-8 -*-
"""urls"""

from django.conf.urls import url

from .views import html_editor_init


urlpatterns = [
    url(r'^html-editor-config.js$', html_editor_init, name='html_editor_init'),
]
