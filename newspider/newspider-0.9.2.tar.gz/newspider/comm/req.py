# -*- coding: utf-8 -*-
import requests

class Req:

    def __init__(self,config):
        self.config = config
        self.session = requests.session()

    def get(self,url,encoding = 'utf8'):
        user_agent = self.config.get('USER_AGENT','newspider/1.0')
        headers = {'user-agent': user_agent}

        r = self.session.get(url, headers=headers)
        print encoding
        r.encoding = encoding

        if r.content is not None:
            return r.content
        else:
            return None


