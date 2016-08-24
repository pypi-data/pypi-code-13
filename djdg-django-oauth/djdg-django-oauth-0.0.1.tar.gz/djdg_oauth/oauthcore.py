# -*- coding: utf-8 -*-
from django.conf import settings as django_settings
import random
import hashlib
from urllib import quote
from .models import OauthApps


def createNoncestr(length=32):
    """产生随机字符串，不长于32位"""
    chars = "abcdefghijklmnopqrstuvwxyz0123456789"
    strs = []
    for x in range(length):
        strs.append(chars[random.randrange(0, len(chars))])
    return "".join(strs)


def formatBizQueryParaMap(paraMap, urlencode):
    """格式化参数，签名过程需要使用"""
    slist = sorted(paraMap)
    buff = []
    for k in slist:
        v = quote(paraMap[k]) if urlencode else paraMap[k]
        buff.append("{0}={1}".format(k, v))

    return "&".join(buff)


def getSign(obj, secret):
    """生成签名"""
    # 签名步骤一：按字典序排序参数,formatBizQueryParaMap已做
    String = formatBizQueryParaMap(obj, False)
    # 签名步骤二：在string后加入KEY
    String = "{0}&secret={1}".format(String, secret)
    # 签名步骤三：MD5加密
    String = hashlib.md5(String).hexdigest()

    # 签名步骤四：所有字符转为大写
    result_ = String.upper()
    print result_
    return result_


def verifySign(obj, secret, signature):
    return signature == getSign(obj, secret)


def get_sign_key(app):
    if hasattr(django_settings, "DJDG_AUTH"):
        auth_list = [
            x for x in django_settings.DJDG_AUTH.get(
                "APPS", []) if x["app"] == app]
        return auth_list[0] if auth_list else None
    else:
        return None


def get_verify_key(appid):
    auth_list = OauthApps.objects.filter(appid=appid)
    return auth_list[0] if auth_list else None


get_verify_key(80145171)


def set_parameters(parameters, app):
    appkeys = get_sign_key(app)
    if not appkeys:
        raise Exception("app secret not find, please check you settings file")
    parameters["appid"] = appkeys["appid"]
    parameters["nonce_str"] = createNoncestr(12)
    return getSign(parameters, appkeys["secret"]), parameters
