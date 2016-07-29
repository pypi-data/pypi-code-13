"""Urls for the pages app."""
from django.conf.urls import url

from .views import PageDetail


app_name = 'pages'  # pylint: disable=invalid-name

urlpatterns = [
    url(r'^(?P<slug>[\w\d-]+)/$',
        PageDetail.as_view(),
        name='page',
        ),
]
