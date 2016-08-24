# -*- coding: utf-8 -*-
from django.conf import settings as django_settings
from .oauthclient import OAuthClient
from django.http.response import HttpResponse
import re


class Http401Response(HttpResponse):

    status_code = 401


class DjdgAuthMiddleware(object):

    def process_request(self, request):
        if hasattr(django_settings, "DJDG_AUTH"):
            full_escape_url = django_settings.DJDG_AUTH.get(
                'FULL_ESCAPE_URL', [])
            regex_escape_url = django_settings.DJDG_AUTH.get(
                'REGEX_ESCAPE_URL', [])
            path = request.path.strip('/')
            if path in full_escape_url:
                return
            for url in regex_escape_url:
                if re.match(url, path):
                    return
        else:
            try:
                auth = OAuthClient()
                if not auth.verify_request(request):
                    return Http401Response('Unauthorized')
            except Exception as e:
                return Http401Response(e.message)
