"""Urls for showing the django_litecrop example."""

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'', views.ExampleView.as_view()),
]
