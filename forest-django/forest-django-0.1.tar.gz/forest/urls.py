from django.conf.urls import url
from forest import views
from forest.views import empty, session, resources, resource, association, stat

urlpatterns = [
    url(r'^$', empty),
    url(r'^sessions$', session),
    url(r'(?i)^(?P<model>[a-z]*)$', resources),
    url(r'(?i)^(?P<model>[a-z]*)/(?P<r_id>[0-9]+)$', resource),
    url(r'(?i)^(?P<model>[a-z]*)/(?P<r_id>[0-9]+)/(?P<association>[a-z]*)$', association),
    url(r'(?i)^stats/(?P<model>[a-z]*)$', stat),
]
