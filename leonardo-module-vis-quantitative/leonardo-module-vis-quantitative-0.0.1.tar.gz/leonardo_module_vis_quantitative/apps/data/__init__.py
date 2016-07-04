
from django.conf.urls import url

from .views import WidgetDataView

urlpatterns = [
    url(r'^data/', WidgetDataView.as_view(), name='vislab_data'),
]
