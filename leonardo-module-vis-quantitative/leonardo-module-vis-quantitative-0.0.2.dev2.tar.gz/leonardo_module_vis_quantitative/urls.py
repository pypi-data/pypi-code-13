
from django.conf.urls import patterns, url

from apps.data.views import WidgetDataView

urlpatterns = [
    url(r'^vis-quantitative-data/time-series/',
        WidgetDataView.as_view(), name='vislab_data'),
]
