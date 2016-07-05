# -*- coding: utf-8 -*-
"""
Django-Linked-Select2 URL configuration.

Add `linked_select2` to your ``urlconf`` **if** you use any 'Model' fields::

    url(r'^select2/', include('linked_select2.urls')),

This way, both Django-Select2 and Django-Linked-Select2 widgets will work.
"""
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from .views import LinkedAutoResponseView

urlpatterns = [
    url(
        r"^fields/auto.json$", LinkedAutoResponseView.as_view(),
        name="django_select2-json"
    ),
]
