# -*- coding: utf-8 -*-
from django.conf.urls import url
# from django.views.generic import TemplateView

from . import views

urlpatterns = [
    # url(r'', TemplateView.as_view(template_name="balystic/base.html")),
    url(r'^blog/$',
        views.CommunityBlogListView.as_view(), name='balystic_blog'),
    url(r'^blog/(?P<slug>[-\w.]+)/$',
        views.CommunityBlogDetailView.as_view(), name='balystic_blog_detail'),
]
