# -*- coding: utf-8 -*-

"""
File:   client.py
Author: CaoKe
Email:  hitakaken@gmail.com
Github: https://github.com/hitakaken
Date:   2016-08-23
Description: WeChat Client
"""
from wechat.oauth2 import Oauth2API


class WechatAPI(Oauth2API):
    def __init__(self, appid=None, secret=None, **kwargs):
        if appid is not None:
            kwargs['appid'] = appid
        if secret is not None:
            kwargs['secret'] = appid
        super(WechatAPI, self).__init__(**kwargs)



