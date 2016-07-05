# -*- coding: UTF-8 -*-
"""
    Created by Régis Eduardo Crestani <regis.crestani@gmail.com> on 05/07/2016.
"""
from django.conf.urls import url, include
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^$', views.charts_map, name='charts-map'),
    url(r'^most-requested[/]?$', views.most_requested, name='most-requested'),
    url(r'^most-bytes[/]?$', views.most_bytes, name='most-bytes'),
    url(r'^most-bytes-average[/]?$', views.most_bytes_average, name='most-bytes-average'),
    url(r'^most-used-bytes[/]?$', views.most_used_bytes, name='most-used-bytes'),
    url(r'^most-used-bytes-average[/]?$', views.most_used_bytes_average, name='most-used-bytes-average'),
    url(r'^most-latency[/]?$', views.most_latency, name='most-latency'),
    url(r'^most-latency-average[/]?$', views.most_latency_average, name='most-latency-average'),
    url(r'^most-used-latency[/]?$', views.most_used_latency, name='most-used-latency'),
    url(r'^most-used-latency-average[/]?$', views.most_used_latency_average, name='most-used-latency-average'),
    # url(r'^products/', include('resource.product.urls')),
]
