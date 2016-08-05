'''
Created on Jun 2, 2015

:author: iitow
'''
import os
import requests
import json
from requests.auth import HTTPBasicAuth
from requests import Request, Session


class Restful(object):
    ''' Perform restful calls with this class
    '''

    def __init__(self, base_url,headers={'content-type': 'application/json'}):
        '''
        Generic class to handle All types of
        Restful requests
        '''
        self.base_url = base_url
        self.headers = headers
        self.request_type = {'GET': requests.get,
                             'PUT': requests.put,
                             'POST': requests.post,
                             'PATCH': requests.patch}

    def send(self,type,ext,**defaults):
        '''
        send http restful requests
        :param type: String, GET,PUT,POST,PATCH
        :param ext: String, url extention
        :return: Dictionary
        '''
        params = defaults.get('params',None)
        data = defaults.get('data',None)
        if params:
            params = json.loads(params)
        if data:
            data = json.loads(data)
            data = json.dumps(data)
        url = "%s/%s" % (self.base_url,ext)
        raw = self.request_type[type](url,
                                      params=params,
                                      headers=self.headers,
                                      data=data)
        code = raw.status_code
        response = raw.content
        return {"code":code,'response':response}
