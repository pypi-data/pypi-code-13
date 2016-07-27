from __future__ import division, unicode_literals, print_function, absolute_import

import json
import sys

import requests
from flask_oauthlib.client import OAuthResponse

sys.path.extend([
    './../',
    './',
    './../../',
])

from flask import Flask
from six.moves.urllib.parse import urlparse, parse_qs
import requests
from requests.auth import _basic_auth_str

try:
    from unittest import mock
except ImportError:
    import mock

import oauth_middleware
from oauth_middleware.providers import zalando

from os.path import dirname, abspath, join

CONF_TEMPLATE = {
    'TESTING': True,
    'SECRET_KEY': 'development',
    'SKIP_AUTH_FOR': [
        '^/login',
        '^/logout$',
        '^/healthcheck$',
        '^/health$',
    ],
    'SUCCESS_LOGIN_PATH': '/',
    'ZALANDO_OAUTH': {
        'request_token_params': {
            'scope': [
                'uid',
                'cn',
            ],
        },
        'credentials_dir': join(abspath(dirname(__file__)), 'fake_credentials'),
        'access_token_method': 'POST',
        'base_url': 'https://example.com/oauth2/',
        'access_token_url': 'access_token?realm=/employees',
        'authorize_url': 'authorize?realm=/employees',
    },
}

test_app = Flask(__name__)


@test_app.route('/')
def index():
    pass


@test_app.route('/healthcheck')
def healthcheck():
    return 'OK'


@test_app.route('/other/very/deep/url')
def other():
    return 'other'


oauth = zalando.make_zalando_oauth()
application = oauth_middleware.make_oauth_wsgi(oauth, test_app.wsgi_app, CONF_TEMPLATE)


def test_auth_skipping():
    client = application.test_client()

    resp = client.get('/healthcheck')

    assert resp.status_code == 200
    assert resp.data == b'OK'


def test_home_initiate_auth():
    client = application.test_client()

    resp = client.get('/')

    assert resp.status_code == 302
    assert resp.headers['Location'] == 'http://localhost/login'


def test_other_initiate_auth():
    client = application.test_client()

    resp = client.get('/other/very/deep/url?q=whatever')

    assert resp.status_code == 302
    assert resp.headers['Location'] == 'http://localhost/login'


def test_login_initiates_oauth():
    client = application.test_client()

    resp = client.get('/login')

    assert resp.status_code == 302
    redirect_to = urlparse(resp.headers['Location'])
    assert redirect_to.netloc == 'example.com'
    assert redirect_to.path == '/oauth2/authorize'
    qs = parse_qs(redirect_to.query)

    assert qs['redirect_uri'] == ['http://localhost/login/oauth_callback']
    assert qs['scope'] == ['uid cn']
    assert qs['realm'] == ['/employees']


def test_auth_via_token_header():
    client = application.test_client()

    with mock.patch('flask_oauthlib.client.OAuthRemoteApp.http_request') as f:
        oauth_resp = requests.Response()
        oauth_resp.status_code = 200
        oauth_resp.code = 200
        oauth_resp._content = json.dumps({
            'access_token': 'existing-token',
        })
        f.return_value = (
            oauth_resp, oauth_resp._content
        )

        resp = client.get(
            '/other/very/deep/url',
            headers={
                'Authorization': 'Bearer existing-token',
            }
        )

        f.assert_called_once_with(
            'https://example.com/oauth2/tokeninfo',
            {
                'Authorization': 'Bearer existing-token',
            },
            data=mock.ANY, method=mock.ANY
        )

    assert resp.status_code == 200
    assert resp.data == b'other'


def test_auth_via_basic_auth():
    client = application.test_client()

    with mock.patch('flask_oauthlib.client.OAuthRemoteApp.http_request') as f:
        oauth_resp = requests.Response()
        oauth_resp.status_code = 200
        oauth_resp.code = 200
        oauth_resp._content = json.dumps({
            'access_token': 'existing-token',
        })
        f.return_value = (
            oauth_resp, oauth_resp._content
        )

        resp = client.get(
            '/other/very/deep/url',
            headers={
                'Authorization': _basic_auth_str('oauth', 'existing-token'),
            }
        )

        f.assert_called_once_with(
            'https://example.com/oauth2/tokeninfo',
            {
                'Authorization': 'Bearer existing-token',
            },
            data=mock.ANY, method=mock.ANY
        )

    assert resp.status_code == 200
    assert resp.data == b'other'


def test_all_domains():
    client = application.test_client()

    resp = client.get(
        '/healthcheck',
        headers={
            'Host': 'example.com',
        }
    )
    assert resp.status_code == 200
    assert resp.data == b'OK'


def test_all_domains_with_protection():
    client = application.test_client()

    resp = client.get(
        '/other/very/deep/url',
        headers={
            'Host': 'example.com',
        }
    )
    assert resp.status_code == 302
