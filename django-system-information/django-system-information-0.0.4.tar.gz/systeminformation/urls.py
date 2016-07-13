# coding:utf-8
from django.conf.urls import patterns


urlpatterns = patterns(
    '',
    (r'^$', 'systeminformation.views.get_information'),
)
