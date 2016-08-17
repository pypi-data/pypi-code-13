# -*- coding: utf-8 -*-
from django.conf import settings


def google_analytics(request):
    return {'GOOGLE_ANALYTICS_ID': getattr(settings, 'GOOGLE_ANALYTICS_ID', None)}


def piwik(request):
    return {'PIWIK_TRACKER_ID': getattr(settings, 'PIWIK_TRACKER_ID', None)}


def site_title(request):
    return {'SITE_TITLE': getattr(settings, 'SITE_TITLE', '')}


def service_url(request):
    return {'SERVICE_URL': getattr(settings, 'SERVICE_URL', '')}
