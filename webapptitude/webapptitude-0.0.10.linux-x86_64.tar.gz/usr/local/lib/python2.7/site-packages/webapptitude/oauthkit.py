"""
Shortcuts for various OAuth processes to authenticate properly.

The methods exposed in this module produce _credential factories_.
Their returned functions will bear a signature as:

    def callback(scope=None):
        return Credentials(...)

Their purpose is to simplify integration with other Google APIs by constructing
reusable credentials components.

Note that testing for these requires secrets files, which are regarded as
sensitive, and therefore not included in the project's codebase.

"""

import os
import sys
import logging

# from oauth2client import __version__ as oauth2client_version
# print "OAuth2 Client Version %r" % (oauth2client_version)

try:
    from oauth2client.contrib import gce, appengine
except ImportError:
    from oauth2client import gce, appengine

try:
    # this works in oauth2client versions > 2.0
    from oauth2client.service_account import ServiceAccountCredentials
except ImportError:
    # NOTE: the oauth2client bundled with AppEngine SDK is version 1.4.12,
    # which hasn't formally exported this kit yet.
    from oauth2client.service_account import \
        _ServiceAccountCredentials as ServiceAccountCredentials


from oauth2client.client import (
    GoogleCredentials,
    flow_from_clientsecrets
)

try:
    import webbrowser
except ImportError:
    webbrowser = None


def mute_logger(name):
    _logger = logging.getLogger(name)
    _logger.addHandler(logging.NullHandler())
    _logger.setLevel(logging.CRITICAL)

mute_logger('oauth2client.client')


def in_production_appengine():
    return os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/')


def p12(keyfile, email):  # TODO: test this
    def callback(scope=None):
        assert isinstance(scope, list)
        return ServiceAccountCredentials.from_p12_keyfile(email, keyfile,
                                                          scopes=scope)
    return callback


def json(keyfile):
    """
    Service account based on JSON credentials.

    Authorized on the basis of a "service account" that's part of a Google
    Cloud project. Requires JSON secrets file.

    Tested & working 2016/06/29;
    """
    def callback(scope=None):
        assert isinstance(scope, list)
        args, kwargs = (keyfile,), dict(scopes=scope)
        if isinstance(keyfile, dict):
            method = ServiceAccountCredentials.from_json_keyfile_dict
        else:
            method = ServiceAccountCredentials.from_json_keyfile_name
        return method(*args, **kwargs)
    return callback


def default():  # TODO: test this
    def callback(scope=None):
        return GoogleCredentials.get_application_default()
    return callback


def flow(path, redirect_uri='urn:ietf:wg:oauth:2.0:oob'):
    """
    Per-user authorization for installed applications and webapps.

    Requires client-secrets JSON, Google treats this as an OAuth 2.0 client ID.
    Tested & working 2016/06/29; requires per-user authorization.
    """
    def callback(scope=None):
        flow_ = flow_from_clientsecrets(path, scope=scope)
        uri = flow_.step1_get_authorize_url(redirect_uri)
        if webbrowser is not None:
            webbrowser.open(uri)
        else:
            print >>sys.stderr, "Please authorize via URL: %s" % uri
        auth_code = raw_input('Enter the auth code: ')
        credentials = flow_.step2_exchange(auth_code)
        return credentials
    return callback


def web():  # TODO: test this
    def callback(scope=None):
        if in_production_appengine():
            return appengine.AppAssertionCredentials(scope)
        else:
            return gce.AppAssertionCredentials(scope)
    return callback





