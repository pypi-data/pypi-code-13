# -*- coding: utf-8 -*-

"""
File:   base.py
Author: CaoKe
Email:  hitakaken@gmail.com
Github: https://github.com/hitakaken
Date:   2016-08-23
Description: WeChat HttpClient Base
"""

from urllib import urlencode, quote
import requests


class BaseAPI(object):
    def __init__(self, **kwargs):
        self.defaults = kwargs
        self.session = requests.Session()
        if 'retry' in self.defaults:
            from requests.adapters import HTTPAdapter
            self.session.mount('http://', HTTPAdapter(max_retries=self.defaults['retry']))
            self.session.mount('https://', HTTPAdapter(max_retries=self.defaults['retry']))

    def validate_required_params(self, required_params, **kwargs):
        missing = []
        for param in required_params:
            if param not in kwargs and param not in self.defaults:
                missing.append(param)
        return len(missing) == 0, missing

    def get_url(self, url, params=None, **kwargs):
        if params is not None:
            query = {}
            for param in params:
                query[param] = kwargs[param] if param in kwargs else self.defaults[param]
            url = url + '?' + urlencode(query)
        return url

    def get(self, url, params=None, **kwargs):
        return self.session.get(self.get_url(url, params=params, **kwargs))
