# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import requests
try:
    from urlparse import urlparse, urlunparse
except ImportError:
    from urllib.parse import urlparse, urlunparse
from .oauthcore import get_verify_key, verifySign, set_parameters
import logging
log = logging.getLogger("oauthlib")


class OAuthClient(object):
    """
    TODO: add docs
    """
    def __init__(self):
        """
        :params server: An instance of oauthlib.oauth2.Server class
        """
        pass

    def _get_escaped_full_path(self, request):
        """
        Django considers "safe" some characters that aren't so for oauthlib.
        We have to search for them and properly escape.
        """
        parsed = list(urlparse(request.get_full_path()))
        return urlunparse(parsed)

    def _extract_params(self, request):
        """
        """
        uri = self._get_escaped_full_path(request)
        http_method = request.method
        headers = self.extract_headers(request)
        body = dict(self.extract_body(request))
        return uri, http_method, body, headers

    def extract_headers(self, request):
        """
        Extracts headers from the Django request object
        :param request: The current django.http.HttpRequest object
        :return: a dictionary with OAuthLib needed headers
        """
        headers = request.META.copy()
        if 'HTTP_AUTHORIZATION' in headers:
            headers['Authorization'] = headers['HTTP_AUTHORIZATION']
        return headers

    def extract_body(self, request):
        """
        Extracts the POST body from the Django request object
        :param request: The current django.http.HttpRequest object
        :return: provided POST parameters
        """
        if request.environ.get("Content-Type") == "application/json":
            return json.loads(request.body.decode('utf-8')).items()
        elif request.method == "GET":
            return request.GET.items()
        else:
            return request.POST.items()

    def verify_request(self, request):
        """
        :param request: The current django.http.HttpRequest object
        """
        uri, http_method, body, headers = self._extract_params(request)
        if not body.get("appid"):
            raise Exception(u"can not find appid in request body")
        keys_obj = get_verify_key(body.get("appid"))
        if not keys_obj:
            raise Exception(
                "can not fetch any settings, please check appid correct")
        signature = headers.get("Authorization")
        request.app_type = keys_obj.app
        return verifySign(body, keys_obj.secret, signature)

    @staticmethod
    def oauth_request(url, method, app, parameters=None, headers=None):
        try:
            signature, parameters = set_parameters(parameters, app)
        except Exception as e:
            log.info(e.message)
            return {"statusCode": 500, "msg": e.message}
        headers_dict = {
            "Accept": "application/json",
            "Content-Type": "application/json;charset=utf-8",
            "Authorization": signature
        }
        headers = headers.update(headers_dict) if headers else headers_dict
        log.info(parameters)
        if method == "get":
            r = requests.request(
                method=method, url=url, headers=headers, params=parameters)
        else:
            r = requests.request(
                method=method, url=url, json=parameters, headers=headers)
        if r.status_code != 200:
            log.error(r.content)
            return {"statusCode": 500, "msg": r.content}
        else:
                try:
                    log.info(r.json())
                    return {"statusCode": 0, "content": r.json()}
                except:
                    log.info(r.content)
                    return {"statusCode": 0, "content": r.content}
