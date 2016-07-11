#!/usr/bin/env python
#-*- coding: utf-8 -*-

import json
import requests
from requests.exceptions import HTTPError
from exceptions import *

class Client(object):

    def __init__(self, api_key):
        self._base_url = 'https://api.niland.io/2.0/'
        self._api_key = api_key

    def get(self, path, params=None):
        return self._request('GET', path, params)

    def post(self, path, data):
        return self._request('POST', path, data)

    def patch(self, path, data):
        return self._request('PATCH', path, data)

    def delete(self, path):
        return self._request('DELETE', path)

    def _request(self, method, path, options=None):
        path = path.lstrip('/')
        path = path.rstrip('/')
        params = {'key': self._api_key}
        url = '%s/%s' % (self._base_url.rstrip('/'), path)

        if 'GET' == method:
            options['key'] = params['key']
            r = requests.get(url, params=options)
        elif 'POST' == method:
            if self._has_to_be_multipart(options):
                data = self._to_multipart(options)
                r = requests.post(url, params=params, data=data['data'], files=data['files'])
            else:
                options = json.dumps(options)
                r = requests.post(url, params=params, data=options, headers={'content-type': 'application/json'})
        elif 'PATCH' == method:
            if self._has_to_be_multipart(options):
                data = self._to_multipart(options)
                r = requests.patch(url, params=params, data=data['data'], files=data['files'])
            else:
                options = json.dumps(options)
                r = requests.patch(url, params=params, data=options, headers={'content-type': 'application/json'})
        elif 'DELETE' == method:
            r = requests.delete(url, params=params)

        try:
            r.raise_for_status()
        except Exception as e:
            if 400 == r.status_code:
                raise BadRequestException(400, r.json())
            elif 401 == r.status_code:
                raise AuthenticationFailedException(401)
            elif 403 == r.status_code:
                raise ForbiddenException(403)
            elif 404 == r.status_code:
                raise NotFoundException(404)
            else:
                raise NilandException(r.status_code)

        if 204 != r.status_code:
            return r.json()

        return None

    def _has_to_be_multipart(self, data):
        for key, value in data.iteritems():
            if self._is_file(value):
                return True
        return False

    def _to_multipart(self, data):
        body = {'files': [], 'data': []}
        for key, value in data.iteritems():
            if self._is_file(value):
                body['files'].append((key, value))
            elif isinstance(value, list):
                for i, element in enumerate(value):
                    body['data'].append(('%s[%s]' % (key, i), element))
            else:
                body['data'].append((key, value))
        return body

    def _is_file(self, data):
        return type(data) is file
