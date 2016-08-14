"""eptrack URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
import views


urlpatterns = [
	url(r'^$', views.home_page, name='home'),
	url(r'^add/$', views.add_page, name='add'),
    url(r'^accounts/login/$', auth_views.login, name='login'),
    url(r'^accounts/logout/$', auth_views.logout, name='logout'),
    url(r'^admin/', include(admin.site.urls)),
    ##Dashboards
    url(r'^(?P<projectid>[0-9]+)/$', views.project_dash, name='project_dash'),    
    url(r'^(?P<projectid>[0-9]+)/(?P<nepaid>[0-9]+)/$', views.nepa_dash, name='nepa_dash'),
    url(r'^(?P<projectid>[0-9]+)/air/(?P<airid>[0-9]+)/$', views.air_dash, name='air_dash'),
    url(r'^(?P<projectid>[0-9]+)/noise/(?P<noiseid>[0-9]+)/$', views.noise_dash, name='noise_dash'),
    url(r'^(?P<projectid>[0-9]+)/ecology/(?P<ecologyid>[0-9]+)/$', views.ecology_dash, name='ecology_dash'),
    url(r'^(?P<projectid>[0-9]+)/aquatics/(?P<aquaticsid>[0-9]+)/$', views.aquatics_dash, name='aquatics_dash'),
    url(r'^(?P<projectid>[0-9]+)/archaeology/(?P<archaeologyid>[0-9]+)/$', views.archaeology_dash, name='archaeology_dash'),
    url(r'^(?P<projectid>[0-9]+)/history/(?P<historyid>[0-9]+)/$', views.history_dash, name='history_dash'),
    url(r'^(?P<projectid>[0-9]+)/pis/$', views.pi_dash, name='pi_dash'),
    url(r'^(?P<projectid>[0-9]+)/pns/$', views.pns_dash, name='pns_dash'),
    ##Edit, make names unique
    url(r'^(?P<projectid>[0-9]+)/edit/$', views.project_edit, name='project_edit'),
    url(r'^(?P<projectid>[0-9]+)/(?P<nepaid>[0-9]+)/edit$', views.nepa_edit, name='nepa_edit'),
    url(r'^(?P<projectid>[0-9]+)/air/(?P<ssid>[0-9]+)/edit$', views.ss_edit, {'ss_type' : 'air', 'form_type' : 'airform'}, name='air_edit'),
    url(r'^(?P<projectid>[0-9]+)/noise/(?P<ssid>[0-9]+)/edit$', views.ss_edit, {'ss_type' : 'noise', 'form_type' : 'noiseform'}, name='noise_edit'),
    url(r'^(?P<projectid>[0-9]+)/ecology/(?P<ssid>[0-9]+)/edit$', views.ss_edit, {'ss_type' : 'ecology', 'form_type' : 'ecoform'}, name='ecology_edit'),
    url(r'^(?P<projectid>[0-9]+)/aquatics/(?P<ssid>[0-9]+)/edit$', views.ss_edit, {'ss_type' : 'aquatics', 'form_type' : 'aquaform'}, name='aquatics_edit'),
    url(r'^(?P<projectid>[0-9]+)/archaeology/(?P<ssid>[0-9]+)/edit$', views.ss_edit, {'ss_type' : 'archaeology', 'form_type' : 'archform'}, name='archaeology_edit'),
    url(r'^(?P<projectid>[0-9]+)/history/(?P<ssid>[0-9]+)/edit$', views.ss_edit, {'ss_type' : 'history', 'form_type' : 'histform'}, name='history_edit'),
    ##Add, make names unique
    url(r'^(?P<projectid>[0-9]+)/nepa/add/$', views.nepa_add, name='nepa_add'),
    url(r'^(?P<projectid>[0-9]+)/air/add/$', views.ss_add, {'ss_type' : 'air', 'form_type' : 'airform'}, name='air_add'),
    url(r'^(?P<projectid>[0-9]+)/noise/add/$', views.ss_add, {'ss_type' : 'noise', 'form_type' : 'noiseform'}, name='noise_add'),
    url(r'^(?P<projectid>[0-9]+)/ecology/add/$', views.ss_add, {'ss_type' : 'ecology', 'form_type' : 'ecoform'}, name='eco_add'),
    url(r'^(?P<projectid>[0-9]+)/aquatics/add/$', views.ss_add, {'ss_type' : 'aquatics', 'form_type' : 'aquaform'}, name='aquatics_add'),
    url(r'^(?P<projectid>[0-9]+)/archaeology/add/$', views.ss_add, {'ss_type' : 'archaeology', 'form_type' : 'archform'}, name='archaeology_add'),
    url(r'^(?P<projectid>[0-9]+)/history/add/$', views.ss_add, {'ss_type' : 'history', 'form_type' : 'histform'}, name='history_add'),
    ]