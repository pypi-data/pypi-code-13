from django.conf.urls import url, include

from ievv_opensource.ievv_elasticsearchbrowser.cradmin import ElasticSearchBrowserCrAdminInstance

urlpatterns = [
    url(r'^', include(ElasticSearchBrowserCrAdminInstance.urls())),
]
