from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from utm_zone_info import viewsets

router = DefaultRouter()
router.register(r'utm-zone-info', viewset=viewsets.UTMZoneInfoViewSet, base_name='utm_zone_info')

urlpatterns = [
    url(r'^', include(router.urls)),
]
