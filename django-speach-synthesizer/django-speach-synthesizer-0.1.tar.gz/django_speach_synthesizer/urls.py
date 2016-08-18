from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^docs/', include('rest_framework_swagger.urls', namespace='docs')),
    url(r'^generate/$', views.generate, name='generate'),
    url(r'^get_file/$', views.get_file, name='get_file'),
]
