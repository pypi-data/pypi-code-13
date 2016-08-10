#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright © 2016 Taylor C. Richberger <taywee@gmx.com>
# This code is released under the license described in the LICENSE file

from __future__ import absolute_import, division, print_function, unicode_literals

from six.moves.urllib.parse import urlparse, urlunparse, quote, urlencode
from six.moves.urllib.request import Request, HTTPPasswordMgrWithDefaultRealm, HTTPBasicAuthHandler, build_opener

import requests
from requests.auth import HTTPBasicAuth

def makeresponse(data):
    if data.text:
        return data.json()
    else:
        return None

class HTTP(object):
    @staticmethod
    def urlquote(string):
        return quote(string, safe='')

    @staticmethod
    def queryencode(query):
        return urlencode(query)

    def __init__(self, scheme, host, port, username, password):
        self.scheme = scheme
        self.host = ':'.join((host, str(port)))
        self.auth = HTTPBasicAuth(username, password)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def GET(self, endpoint):
        response = requests.get(urlunparse((self.scheme, self.host, endpoint, '', '', '')), headers={'Content-Type': 'application/json'}, auth=self.auth)
        response.raise_for_status()
        return makeresponse(response)

    def DELETE(self, endpoint):
        response = requests.delete(urlunparse((self.scheme, self.host, endpoint, '', '', '')), headers={'Content-Type': 'application/json'}, auth=self.auth)
        response.raise_for_status()
        return makeresponse(response)

    def PUT(self, endpoint, data=None):
        if data is None:
            data = dict()

        response = requests.put(urlunparse((self.scheme, self.host, endpoint, '', '', '')), headers={'Content-Type': 'application/json'}, json=data, auth=self.auth)
        response.raise_for_status()
        return makeresponse(response)

    def POST(self, endpoint, data=None):
        if data is None:
            data = dict()

        response = requests.post(urlunparse((self.scheme, self.host, endpoint, '', '', '')), headers={'Content-Type': 'application/json'}, json=data, auth=self.auth)
        response.raise_for_status()
        return makeresponse(response)
