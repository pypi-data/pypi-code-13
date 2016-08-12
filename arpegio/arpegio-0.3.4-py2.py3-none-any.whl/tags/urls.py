"""Urls for the tags app."""
from django.conf.urls import url

from .views import TagDetail


app_name = 'tags'  # pylint: disable=invalid-name

urlpatterns = [
    url(r'^(?P<slug>[\w\d-]+)/$',
        TagDetail.as_view(),
        name='tag',
        ),
]
