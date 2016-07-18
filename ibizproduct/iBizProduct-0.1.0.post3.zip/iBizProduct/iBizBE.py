from __future__ import unicode_literals
import requests
import os
from builtins import dict
from future.utils import raise_with_traceback

class iBizBE(object):
    __PRODUCTION_API = 'https://backend.ibizapi.com:8888'
    __STAGING_API = 'https://backendbeta.ibizapi.com:8888'

    def __init__(self, isDev, verifySSL):
        self._client_opts = dict(defaults=dict(verify=verifySSL))
        self._IsDev = isDev
    
    def getIsDev(self):
        return self._IsDev

    def setIsDev(self, value):
        self._IsDev = value

    IsDev = property(getIsDev,setIsDev)

    def call(self, endpoint, action = 'VIEW', params = {}):
        uri = self.EndpointFormatter(self._IsDev, endpoint, action)
        return self.JsonCall(uri, params)

    def EndpointFormatter(self, isDev, endpoint, action):
        if isDev:
            return iBizBE.__STAGING_API + '/JSON/' + endpoint + '?action=' + action
        else:
            return iBizBE.__PRODUCTION_API + '/JSON/' + endpoint + '?action=' + action

    def JsonCall(self, uri, params):
        response = requests.post(url=uri, data=None, json=params,verify=self._client_opts.get('verify'))
        result = response.json()

        if response.status_code == 500:
            if result.get('error') != None:
                raise_with_traceback(ValueError(result.get('error')))
            else:
                raise_with_traceback(requests.exceptions.ContentDecodingError)
        
        return result