# -*- coding: utf-8 -*-
class Base:
    def __init__(self, **kwargs):
        self.defaults = kwargs
        self.session = requests.Session()
        if 'retry' in self.defaults:
            from requests.adapters import HTTPAdapter
            self.session.mount('http://', HTTPAdapter(max_retries=self.defaults['retry']))
            self.session.mount('https://', HTTPAdapter(max_retries=self.defaults['retry']))