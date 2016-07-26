DEBUG = True
TESTING = True
SECRET_KEY = 'development'
PREFERRED_URL_SCHEME = 'https'
SERVER_NAME = 'localhost:8080'
SKIP_AUTH_FOR = [
    '^/login',
    '^/logout$',
    '^/healthcheck$',
    '^/healt$',
]
SUCCESS_LOGIN_PATH = '/'
ZALANDO_OAUTH = {
    'request_token_params': {
        'scope': [
            'uid',  # login
            'cn',  # full name
            # Reversed from auth.zalando.com but not doesn't work
            # 'givenName',        # first name
            # 'sn',               # last name
            # 'mail',             # email
            # 'telephoneNumber'   # phone
        ],
    },
    'credentials_dir': 'credentials/pypi-dev/',
    'access_token_method': 'POST',
    'base_url': 'https://auth.zalando.com/oauth2/',
    'access_token_url': 'access_token?realm=/employees',
    'authorize_url': 'authorize?realm=/employees',
}

