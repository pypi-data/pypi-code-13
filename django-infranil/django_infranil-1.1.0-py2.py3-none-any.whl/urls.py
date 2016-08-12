from __future__ import unicode_literals

from django.conf.urls import url
from .views import InfranilView


urlpatterns = [
    url(r'^(?P<path>.*)$', InfranilView.as_view()),
]
