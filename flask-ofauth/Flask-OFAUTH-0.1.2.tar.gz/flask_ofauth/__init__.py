# coding:utf-8

import os
import re
import json
import fnmatch
import requests
import traceback
from functools import wraps
from flask import g, jsonify, session, redirect, request

__author__ = 'lufeng'

token_re = re.compile(r"\??\b_token=\w+&?")


def res_json(code, data, message, success, **kwargs):
    res = jsonify(
        code=code,
        data=data,
        message=message,
        success=success,
        **kwargs
    )
    if str(code) in ["200", "401", "403"]:
        res.status_code = code
    return res


class Auth(object):
    """
    """

    def __init__(self, cache, app=None, url=None, app_id=None, app_secret=None):
        self.cache = cache
        self.app = app
        self.url = url
        self.app_id = app_id
        self.app_secret = app_secret

    def init_app(self, app):
        """
        初始化cmdb客户端
        """
        self.app = app
        self.url = self.app.config.get("SSO_URL")
        self.app_id = self.app.config.get("SSO_APP_ID")
        self.app_secret = self.app.config.get("SSO_APP_SECRET")
        self.version = self.app.config.get("SSO_API_VERSION", "v2")
        if not all([self.url, self.app_id, self.app_secret]):
            raise Exception(u"all SSO_URL, SSO_APP_ID, SSO_APP_SECRET is required")

    def decision(self, allows, permissions):
        """
        针对传入的参数判断是否有权限
        :param allows:
        :param permissions:
        :return:
        """
        includes = [p for p in permissions if 'include' in p]
        excludes = [p for p in permissions if 'exclude' in p]
        in_priority = set([])
        ex_priority = set([])
        for item in allows:
            for i in includes:
                pattern, resource, priority = i.split(':')
                regx = re.compile(resource)
                if fnmatch.fnmatch(item, resource) or regx.match(item):
                    in_priority.add(int(priority))
            for e in excludes:
                pattern, resource, priority = e.split(':')
                regx = re.compile(resource)
                if fnmatch.fnmatch(item, resource) or regx.match(item):
                    ex_priority.add(int(priority))
        if in_priority:
            if ex_priority:
                return max(in_priority) > max(ex_priority)
            return True
        else:
            return False

    def get_user_info(self, token):
        """

        """
        request = requests.session()
        url = '%s/account/user_info.json?token=%s&secret=%s&app=%d&version=%s' % (
            self.url,
            token,
            self.app_secret,
            self.app_id,
            self.version
        )
        req = request.get(url)
        return req.json()

    def get_secret_info(self, secret_id, signature):
        """
        """
        url = '%s/account/secret_info.json' % self.url
        body = {
            "version": self.version,
            "secretId": secret_id,
            "signature": signature,
            "appSecret": self.app_secret,
            "appId": self.app_id
        }
        request = requests.session()
        req = request.post(url, body)
        return req.json()

    def required(self, permissions, **kwargs):
        if not (isinstance(permissions, list) or isinstance(permissions, tuple)):
            permissions = [permissions, ]

        if "super.admin" not in permissions:
            permissions.append("super.admin")

        def wrap(func):
            @wraps(func)
            def inner_wrap(*args, **kwargs):
                if hasattr(g, 'user'):
                    if self.decision(permissions, g.user['permissions']):
                        return func(*args, **kwargs)
                if len(permissions) == 0:
                    return func(*args, **kwargs)
                msg = u"没有权限访问"
                return res_json(**{"code": 403, "data": "", "message": unicode(msg), "success": False})

            return inner_wrap

        return wrap

    def login_required(self, login_url):
        def wrap(func):
            @wraps(func)
            def inner_wrap(*args, **kwargs):
                if session.get('user_token'):
                    return func(*args, **kwargs)
                if not self.app.config.get('SSO_ENABLE'):
                    return func(*args, **kwargs)
                return redirect(login_url)

            return inner_wrap

        return wrap

    def allow(self, permissions):
        if not (isinstance(permissions, list) or isinstance(permissions, tuple)):
            permissions = [permissions, ]
        if "super.admin" not in permissions:
            permissions.append("super.admin")

        if not hasattr(g, 'user'):
            return False
        if self.decision(permissions, g.user['permissions']) or len(permissions) == 0:
            return True
        return False

    def load_user(self):
        if not self.app.config.get('SSO_ENABLE'):
            g.user = self.app.config.get("LOCAL_USER")
            session["user_token"] = ""
            return

        if session.get('user_token'):
            ukey = "%s:Auth:UserInfo:%s" % (self.app.config["PROJECT_NAME"], session.get('user_token'))
            user_info = self.cache.get(ukey)
            if user_info:
                g.user = user_info
                g.user["is_leader"] = False
                g.user["token"] = session["user_token"]
                if token_re.findall(request.url):
                    return redirect(token_re.sub("", request.url))
            else:
                try:
                    resp = self.get_user_info(session["user_token"])
                    if resp['code'] == 200:
                        self.cache.set(ukey, resp["data"], timeout=self.app.config["AUTH_CACHE_TIMEOUT"])
                        g.user = resp["data"]
                        g.user["is_leader"] = False
                        if token_re.findall(request.url):
                            return redirect(token_re.sub("", request.url))
                    elif resp['code'] == 403:
                        resp = jsonify({"code": 401, "data": "", "message": "Login Fail", "success": False})
                        resp.status_code = 401
                        return resp
                    else:
                        resp = jsonify({"code": 401, "data": "", "message": "Need Login", "success": False})
                        resp.status_code = 401
                        return resp
                except Exception, e:
                    resp = jsonify({"code": 401, "data": "", "message": "Need Login", "success": False})
                    resp.status_code = 401
                    return resp
        else:
            resp = jsonify({"code": 401, "data": "", "message": "Need Login", "success": False})
            resp.status_code = 401
            return resp

    def load_api(self):
        """
        """
        if not self.app.config.get('SSO_ENABLE'):
            g.user = self.app.config.get("LOCAL_USER")
            return
        # 必须要提供两个头参数
        secretid = request.headers.get("x-secretid") or request.values.get("x-secretid")
        signature = request.headers.get("x-signature") or request.values.get("x-signature")
        token = session.get('user_token') or request.headers.get("x-token") or request.values.get("token")
        if not token:
            ukey = "%s:Auth:UserInfo:%s" % (self.app.config["PROJECT_NAME"], secretid)
            user_info = self.cache.get(ukey)
            if user_info:
                g.user = user_info
                if token_re.findall(request.url):
                    return redirect(token_re.sub("", request.url))
            if secretid and signature:
                try:
                    resp = self.get_secret_info(secretid, signature)
                    if resp['code'] == 200:
                        g.user = resp["data"]
                        self.cache.set(ukey, resp["data"], timeout=self.app.config["AUTH_CACHE_TIMEOUT"])
                        if token_re.findall(request.url):
                            return redirect(token_re.sub("", request.url))
                    else:
                        return res_json(
                            code=resp['code'],
                            data="",
                            message=resp.get("message"),
                            success=False
                        )
                except Exception, e:
                    self.app.logger.error(traceback.format_exc())
                    return res_json(
                        code=500,
                        data="",
                        message=e.message,
                        success=False
                    )
            else:
                return res_json(
                    code=403,
                    data="",
                    message="auth fail,x-secretid and x-signature or x-token in headers or query_string is required.",
                    success=False
                )
        else:
            if not self.app.config.get('SSO_ENABLE'):
                g.user = self.app.config.get("LOCAL_USER")
                return
            ukey = "%s:Auth:UserInfo:%s" % (self.app.config["PROJECT_NAME"], token)
            user_info = self.cache.get(ukey)
            if user_info:
                g.user = user_info
                if token_re.findall(request.url):
                    return redirect(token_re.sub("", request.url))
            try:
                resp = self.get_user_info(token)
                if resp['code'] == 200:
                    g.user = resp["data"]
                    self.cache.set(ukey, resp["data"], timeout=self.app.config["AUTH_CACHE_TIMEOUT"])
                    if token_re.findall(request.url):
                        return redirect(token_re.sub("", request.url))
                else:
                    resp = jsonify({
                        "code": 403,
                        "data": "",
                        "message": "auth fail,x-secretid and x-signature or x-token in headers or query_string is required.",
                        "success": False})
                    return resp
            except Exception, e:
                resp = jsonify({"code": 403, "data": "", "message": e.message, "success": False})
                return resp
