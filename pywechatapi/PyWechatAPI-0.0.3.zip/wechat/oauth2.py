# -*- coding: utf-8 -*-

"""
File:   oauth2.py
Author: CaoKe
Email:  hitakaken@gmail.com
Github: https://github.com/hitakaken
Date:   2016-08-23
Description: WeChat OAuth2 API
"""
import json

from wechat.base import BaseAPI

# https://mp.weixin.qq.com/wiki/4/9ac2e7b1f1d22e9e57260f6553822520.html
# 第一步：用户同意授权，获取code
AUTHORIZE_URL = 'https://open.weixin.qq.com/connect/oauth2/authorize'
AUTHORIZE_QUERY_PARAMS = ['appid', 'redirect_uri', 'response_type', 'scope', 'state']
SCOPE_BASE = 'snsapi_base'
SCOPE_USERINFO = 'snsapi_userinfo'
# 第二步：通过code换取网页授权access_token
EXCHANGE_CODE_URL = 'https://api.weixin.qq.com/sns/oauth2/access_token'
EXCHANGE_CODE_QUERY_PARAMS = ['appid', 'secret', 'code', 'grant_type']
# 第三步：刷新access_token（如果需要）
Refresh_TOKEN_URL = 'https://api.weixin.qq.com/sns/oauth2/refresh_token'
Refresh_TOKEN_QUERY_PARAMS = ['appid', 'grant_type', 'refresh_token']
# 第四步：拉取用户信息(需scope为 snsapi_userinfo)
GET_USER_INFO_URL = 'https://api.weixin.qq.com/sns/userinfo'
GET_USER_INFO_QUERY_PARAMS = ['access_token', 'openid', 'lang']
# 附：检验授权凭证（access_token）是否有效
VALIDATE_ACCESS_TOKEN_URL = 'https://api.weixin.qq.com/sns/auth'
VALIDATE_ACCESS_TOKEN_QUERY_PARAMS = ['access_token', 'openid']


class Oauth2API(BaseAPI):
    def __init__(self, **kwargs):
        super(Oauth2API, self).__init__(**kwargs)

    def get_authorize_url(self, state=None, **kwargs):
        """第一步：用户同意授权，获取code
        在确保微信公众账号拥有授权作用域（scope参数）的权限的前提下（服务号获得高级接口后，默认拥有scope参数中的snsapi_base和snsapi_userinfo），引导关注者打开如下页面：
            https://open.weixin.qq.com/connect/oauth2/authorize?appid=APPID&redirect_uri=REDIRECT_URI&response_type=code&scope=SCOPE&state=STATE#wechat_redirect
            若提示“该链接无法访问”，请检查参数是否填写错误，是否拥有scope参数对应的授权作用域权限。

        参数说明
            参数	是否必须	说明
            appid	是	公众号的唯一标识
            redirect_uri	是	授权后重定向的回调链接地址，请使用urlencode对链接进行处理
            response_type	是	返回类型，请填写code
            scope	是	应用授权作用域，snsapi_base （不弹出授权页面，直接跳转，只能获取用户openid），snsapi_userinfo （弹出授权页面，可通过openid拿到昵称、性别、所在地。并且，即使在未关注的情况下，只要用户授权，也能获取其信息）
            state	否	重定向后会带上state参数，开发者可以填写a-zA-Z0-9的参数值，最多128字节
            #wechat_redirect	是	无论直接打开还是做页面302重定向时候，必须带此参数

        用户同意授权后
            如果用户同意授权，页面将跳转至 redirect_uri/?code=CODE&state=STATE。若用户禁止授权，则重定向后不会带上code参数，仅会带上state参数redirect_uri?state=STATE

        code说明 ：
            code作为换取access_token的票据，每次用户授权带上的code将不一样，code只能使用一次，5分钟未被使用自动过期。
        """
        if state is not None:
            kwargs['state'] = state
        if 'response_type' not in kwargs and 'response_type' not in self.defaults:
            kwargs['response_type'] = 'code'
        if 'scope' not in kwargs and 'scope' not in self.defaults:
            kwargs['scope'] = SCOPE_BASE
        valid, missing = self.validate_required_params(AUTHORIZE_QUERY_PARAMS, **kwargs)
        if not valid:
            raise Exception('Missing Required Query Params:' + json.dumps(missing))
        return self.get_url(AUTHORIZE_URL, AUTHORIZE_QUERY_PARAMS,  **kwargs)

    @staticmethod
    def is_authorized(request_args):
        """判断用户是否授权
        用户如果没有授权，则request.args不存在code
        """
        return request_args is not None and type(request_args) == dict and 'code' in request_args

    def exchange_code(self, code=None, **kwargs):
        """第二步：通过code换取网页授权access_token

        首先请注意，这里通过code换取的是一个特殊的网页授权access_token,与基础支持中的access_token（该access_token用于调用其他接口）不同。公众号可通过下述接口来获取网页授权access_token。如果网页授权的作用域为snsapi_base，则本步骤中获取到网页授权access_token的同时，也获取到了openid，snsapi_base式的网页授权流程即到此为止。
        尤其注意：由于公众号的secret和获取到的access_token安全级别都非常高，必须只保存在服务器，不允许传给客户端。后续刷新access_token、通过access_token获取用户信息等步骤，也必须从服务器发起。

        请求方法
            获取code后，请求以下链接获取access_token：
            https://api.weixin.qq.com/sns/oauth2/access_token?appid=APPID&secret=SECRET&code=CODE&grant_type=authorization_code

        参数说明
            appid	是	公众号的唯一标识
            secret	是	公众号的appsecret
            code	是	填写第一步获取的code参数
            grant_type	是	填写为authorization_code

            返回说明
            正确时返回的JSON数据包字段如下：
                access_token	网页授权接口调用凭证,注意：此access_token与基础支持的access_token不同
                expires_in	access_token接口调用凭证超时时间，单位（秒）
                refresh_token	用户刷新access_token
                openid	用户唯一标识，请注意，在未关注公众号时，用户访问公众号的网页，也会产生一个用户和公众号唯一的OpenID
                scope	用户授权的作用域，使用逗号（,）分隔
            错误时微信会返回JSON数据包如下（示例为Code无效错误）:
                {"errcode":40029,"errmsg":"invalid code"}
        """
        if code is not None:
            kwargs['code'] = code
        if 'grant_type' not in kwargs and 'grant_type' not in self.defaults:
            kwargs['grant_type'] = 'authorization_code'
        valid, missing = self.validate_required_params(EXCHANGE_CODE_QUERY_PARAMS, **kwargs)
        if not valid:
            raise Exception('Missing Required Query Params:' + json.dumps(missing))
        resp = self.get(EXCHANGE_CODE_URL, EXCHANGE_CODE_QUERY_PARAMS, **kwargs)
        resp.encoding = 'utf-8'
        result = json.loads(resp.text)
        if 'errcode' in result:
            raise Exception(resp.text)
        return result

    def refresh_token(self, refresh_token=None, **kwargs):
        """第三步：刷新access_token（如果需要）

        由于access_token拥有较短的有效期，当access_token超时后，可以使用refresh_token进行刷新，refresh_token拥有较长的有效期（7天、30天、60天、90天），当refresh_token失效的后，需要用户重新授权。

        请求方法
            获取第二步的refresh_token后，请求以下链接获取access_token：
            https://api.weixin.qq.com/sns/oauth2/refresh_token?appid=APPID&grant_type=refresh_token&refresh_token=REFRESH_TOKEN

        参数说明
            appid	是	公众号的唯一标识
            grant_type	是	填写为refresh_token
            refresh_token	是	填写通过access_token获取到的refresh_token参数

        返回说明
            正确时返回的JSON数据包字段如下：
                access_token	网页授权接口调用凭证,注意：此access_token与基础支持的access_token不同
                expires_in	access_token接口调用凭证超时时间，单位（秒）
                refresh_token	用户刷新access_token
                openid	用户唯一标识
                scope	用户授权的作用域，使用逗号（,）分隔

            错误时微信会返回JSON数据包如下（示例为Code无效错误）:
                {"errcode":40029,"errmsg":"invalid code"}
        """
        if refresh_token is not None:
            kwargs['refresh_token'] = refresh_token
        if 'grant_type' not in kwargs and 'grant_type' not in self.defaults:
            kwargs['grant_type'] = 'refresh_token'
        valid, missing = self.validate_required_params(Refresh_TOKEN_QUERY_PARAMS, **kwargs)
        if not valid:
            raise Exception('Missing Required Query Params:' + json.dumps(missing))
        resp = self.get(Refresh_TOKEN_URL, Refresh_TOKEN_QUERY_PARAMS, **kwargs)
        resp.encoding = 'utf-8'
        result = json.loads(resp.text)
        if 'errcode' in result:
            raise Exception(resp.text)
        return result

    def get_user_info(self, access_token=None, openid=None, **kwargs):
        """第四步：拉取用户信息(需scope为 snsapi_userinfo)

        如果网页授权作用域为snsapi_userinfo，则此时开发者可以通过access_token和openid拉取用户信息了。

        请求方法
            http：GET（请使用https协议）
            https://api.weixin.qq.com/sns/userinfo?access_token=ACCESS_TOKEN&openid=OPENID&lang=zh_CN

        参数说明
            access_token	网页授权接口调用凭证,注意：此access_token与基础支持的access_token不同
            openid	用户的唯一标识
            lang	返回国家地区语言版本，zh_CN 简体，zh_TW 繁体，en 英语

        返回说明
            正确时返回的JSON数据字段如下：
            openid	用户的唯一标识
            nickname	用户昵称
            sex	用户的性别，值为1时是男性，值为2时是女性，值为0时是未知
            province	用户个人资料填写的省份
            city	普通用户个人资料填写的城市
            country	国家，如中国为CN
            headimgurl	用户头像，最后一个数值代表正方形头像大小（有0、46、64、96、132数值可选，0代表640*640正方形头像），用户没有头像时该项为空。若用户更换头像，原有头像URL将失效。
            privilege	用户特权信息，json 数组，如微信沃卡用户为（chinaunicom）
            unionid	只有在用户将公众号绑定到微信开放平台帐号后，才会出现该字段。详见：获取用户个人信息（UnionID机制）

            错误时微信会返回JSON数据包如下（示例为openid无效）:
            {"errcode":40003,"errmsg":" invalid openid "}
        """
        if access_token is not None:
            kwargs['access_token'] = access_token
        if openid is not None:
            kwargs['openid'] = openid
        if 'lang' not in kwargs and 'lang' not in self.defaults:
            kwargs['lang'] = 'zh_CN'
        valid, missing = self.validate_required_params(GET_USER_INFO_QUERY_PARAMS, **kwargs)
        if not valid:
            raise Exception('Missing Required Query Params:' + json.dumps(missing))
        resp = self.get(GET_USER_INFO_URL, GET_USER_INFO_QUERY_PARAMS, **kwargs)
        resp.encoding = 'utf-8'
        result = json.loads(resp.text)
        if 'errcode' in result:
            raise Exception(resp.text)
        return result

    def validate_access_token(self, access_token=None, openid=None, **kwargs):
        """附：检验授权凭证（access_token）是否有效

        请求方法
            http：GET（请使用https协议）
            https://api.weixin.qq.com/sns/auth?access_token=ACCESS_TOKEN&openid=OPENID

        参数说明
            access_token	网页授权接口调用凭证,注意：此access_token与基础支持的access_token不同
            openid	用户的唯一标识

        返回说明
        正确的Json返回结果：
            { "errcode":0,"errmsg":"ok"}
        错误时的Json返回示例：
            { "errcode":40003,"errmsg":"invalid openid"}
        """
        if access_token is not None:
            kwargs['access_token'] = access_token
        if openid is not None:
            kwargs['openid'] = openid
        valid, missing = self.validate_required_params(VALIDATE_ACCESS_TOKEN_QUERY_PARAMS, **kwargs)
        if not valid:
            raise Exception('Missing Required Query Params:' + json.dumps(missing))
        resp = self.get(VALIDATE_ACCESS_TOKEN_URL, VALIDATE_ACCESS_TOKEN_QUERY_PARAMS, **kwargs)
        resp.encoding = 'utf-8'
        result = json.loads(resp.text)
        if 'errcode' in result and result['errcode'] > 0:
            raise Exception(resp.text)
        return result


