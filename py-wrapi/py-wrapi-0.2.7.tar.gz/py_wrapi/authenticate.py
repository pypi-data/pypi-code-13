import requests
import os
import subprocess
import urllib
import base64

from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run_flow, argparser
from oauth2client.file import Storage

def google_auth(client_id, client_secret, scope):
    flow = OAuth2WebServerFlow(client_id=client_id,
                           client_secret=client_secret,
                           scope=scope,
                           redirect_uri='http://localhost')
    storage = Storage('creds.data')
    flags = argparser.parse_args(args=[])
    credentials = run_flow(flow, storage, flags)
    access_token = credentials.access_token
    os.remove('creds.data')
    return access_token

def spotify_auth(client_id, client_secret, scope):
    OAUTH_AUTHORIZE_URL = 'https://accounts.spotify.com/authorize'
    OAUTH_TOKEN_URL = 'https://accounts.spotify.com/api/token'
    REDIRECT_URI = 'http://localhost/'
    if isinstance(scope, list):
        scope = ' '.join(scope)
    urlparams = urllib.parse.urlencode({
        'client_id': client_id,
        'response_type': 'code',
        'redirect_uri': REDIRECT_URI,
        'scope': scope
    })
    auth_url = '%s?%s' % (OAUTH_AUTHORIZE_URL, urlparams)
    subprocess.call(["open", auth_url])
    code = input("Copy paste the URL you were directed to:\n>> ").split("?code=")[1].split("&")[0]

    body = {
        'redirect_uri': REDIRECT_URI,
        'code': code,
        'grant_type': 'authorization_code',
        'scope': scope
    }
    auth_header = base64.b64encode(str(client_id + ':' + client_secret).encode())
    headers = {'Authorization': 'Basic %s' % auth_header.decode()}
    token_info = requests.post(OAUTH_TOKEN_URL, data=body,
            headers=headers, verify=True).json()
    return token_info['access_token']
