# -*- coding: utf-8 -*-


import json
import urllib2

from flask import current_app
from werkzeug import url_encode


__all__ = ["WeixinLogin", "add_query"]


def add_query(url, args):
    if not args:
        return url
    return url + ('?' in url and '&' or '?') + url_encode(args)


class WeixinLogin(object):

    def __init__(self, app=None):
        self.opener = urllib2.build_opener(urllib2.HTTPSHandler())

        if app is None:
            self.app = current_app
        else:
            self.init_app(app)
            self.app = app

    def init_app(self, app):
        app.config.setdefault("WEIXIN_APP_ID", "")
        app.config.setdefault("WEIXIN_APP_SECRET", "")

    def _get_app_id(self):
        return self.app.config["WEIXIN_APP_ID"]

    def _set_app_id(self, app_id):
        self.app.config["WEIXIN_APP_ID"] == app_id

    app_id = property(_get_app_id, _set_app_id)
    del _get_app_id, _set_app_id

    def _get_app_secret(self):
        return self.app.config["WEIXIN_APP_SECRET"]

    def _set_app_secret(self, app_secret):
        self.app.config["WEIXIN_APP_SECRET"] = app_secret

    app_secret = property(_get_app_secret, _set_app_secret)
    del _get_app_secret, _set_app_secret

    def authorize(self, callback, scope="snsapi_base", state=None):
        """
        生成微信认证地址并且跳转

        :param callback: 跳转地址
        :param scope: 微信认证方式，有`snsapi_base`跟`snsapi_userinfo`两种
        :param state: 认证成功后会原样带上此字段
        """
        url = "https://open.weixin.qq.com/connect/oauth2/authorize"

        assert scope in ["snsapi_base", "snsapi_userinfo"]
        data = dict()
        data.setdefault("appid", self.app_id)
        data.setdefault("redirect_uri", callback)
        data.setdefault("response_type", "code")
        data.setdefault("scope", scope)
        if state:
            data.setdefault("state", state)
        data = [(k, data[k]) for k in sorted(data.keys()) if data[k]]
        s = "&".join("=".join(kv) for kv in data if kv[1])
        return "{0}?{1}#wechat_redirect".format(url, s)

    def get(self, url):
        req = urllib2.Request(url)
        resp = self.opener.open(req)
        return json.loads(resp.read())

    def access_token(self, code):
        url = "https://api.weixin.qq.com/sns/oauth2/access_token"
        args = dict()
        args.setdefault("appid", self.app_id)
        args.setdefault("secret", self.app_secret)
        args.setdefault("code", code)
        args.setdefault("grant_type", "authorization_code")

        url = add_query(url, args)
        return self.get(url)

    def refresh_token(self, refresh_token):
        url = "https://api.weixin.qq.com/sns/oauth2/refresh_token"
        args = dict()
        args.setdefault("appid", self.app_id)
        args.setdefault("grant_type", "refresh_token")
        args.setdefault("refresh_token", refresh_token)

        url = add_query(url, args)
        return self.get(url)

    def user_info(self, access_token, openid):
        """
        获取用户信息

        :param access_token: 令牌
        :param openid: 用户id，每个应用内唯一
        """
        url = "https://api.weixin.qq.com/sns/userinfo"
        args = dict()
        args.setdefault("access_token", access_token)
        args.setdefault("openid", openid)
        args.setdefault("lang", "zh_CN")

        url = add_query(url, args)
        return self.get(url)
