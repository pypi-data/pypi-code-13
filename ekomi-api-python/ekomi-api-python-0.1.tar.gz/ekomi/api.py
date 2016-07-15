# coding=utf-8
"""
ekomi API
"""
__copyright__ = 'Copyright 2016, DNest'

import requests
import json


WEBSERVICE_URL = 'http://api.ekomi.de/v3/'


class EkomiAPI(object):
    id = ''
    pw = ''

    def __init__(self, id, pw):
        self.id = id
        self.pw = pw

    def _make_request(self, url_method, params, method='GET', payload={}):
        params.update({
            'auth': '%s|%s' % (self.id, self.pw),
            'version': 'cust-1.0.0',
            'charset': 'utf-8',
            'type': 'json'
        })
        response = requests.request(method, WEBSERVICE_URL + url_method, data=payload,
                                    params=params)
        response_dict = json.loads(response.content)
        return response_dict

    def put_order(self, order_id, date):
        params = {
            'order_id': order_id,
            'ordertimestamp': date.strftime('%Y-%m-%d %H:%M:%S')
        }
        return self._make_request('putOrder', params)
