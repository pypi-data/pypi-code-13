# -*- coding: utf-8 -*-
from django.conf.urls import url
# from django.views.generic import TemplateView

from . import views

urlpatterns = [
    # url(r'', TemplateView.as_view(template_name="balystic/base.html")),
    url(r'^users/$', views.CommunityUserList.as_view(),
        name='balystic_user_list'),
    url(r'^users/(?P<username>[-\w.]+)$', views.CommunityUserDetail.as_view(),
        name='balystic_user_detail'),
    url(r'^blog/$',
        views.CommunityBlogListView.as_view(), name='balystic_blog'),
    url(r'^blog/(?P<slug>[-\w.]+)/$',
        views.CommunityBlogDetailView.as_view(), name='balystic_blog_detail'),
    url(r'^qa/$',
        views.CommunityQAListView.as_view(), name='balystic_qa'),
    url(r'^qa/(?P<pk>\d+)/$',
        views.CommunityQADetailView.as_view(), name='balystic_qa_detail'),
]
