# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    url(
        regex="^Contact/~create/$",
        view=views.ContactCreateView.as_view(),
        name='Contact_create',
    ),
    url(
        regex="^Contact/(?P<pk>\d+)/~delete/$",
        view=views.ContactDeleteView.as_view(),
        name='Contact_delete',
    ),
    url(
        regex="^Contact/(?P<pk>\d+)/$",
        view=views.ContactDetailView.as_view(),
        name='Contact_detail',
    ),
    url(
        regex="^Contact/(?P<pk>\d+)/~update/$",
        view=views.ContactUpdateView.as_view(),
        name='Contact_update',
    ),
    url(
        regex="^Contact/$",
        view=views.ContactListView.as_view(),
        name='Contact_list',
    ),
	]
