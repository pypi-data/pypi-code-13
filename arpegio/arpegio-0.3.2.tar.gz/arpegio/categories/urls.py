"""Urls for the categories app."""
from django.conf.urls import url

from .views import CategoryDetail


app_name = 'categories'  # pylint: disable=invalid-name

urlpatterns = [
    url(r'^(?P<slug>[\w\d-]+)/$',
        CategoryDetail.as_view(),
        name='category',
        ),
]
