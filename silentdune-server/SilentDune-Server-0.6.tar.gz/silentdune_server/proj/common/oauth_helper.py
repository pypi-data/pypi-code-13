#
# Authors: Robert Abram <robert.abram@entpack.com>
#
# Copyright (C) 2015 EntPack
# see file 'COPYING' for use and warranty information
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import json
from oauthlib.common import generate_token
from oauth2_provider.settings import oauth2_settings
from oauth2_provider.models import AccessToken, RefreshToken
from oauth2_provider.models import get_application_model
from oauth2_provider.compat import get_user_model
from django.utils.timezone import now, timedelta
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from cryptography.fernet import Fernet


# http://httplambda.com/a-rest-api-with-django-and-oauthw-authentication/


def build_token_dict(token):
    """
    Takes an AccessToken instance as an argument and returns a dictionary object.

    :param token: access token object from create_access_token()
    :return: dictionary object
    """
    return {
        'access_token': token.token,
        'expires_in': oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS,
        'token_type': 'Bearer',
        'refresh_token': token.refresh_token.token,
        'scope': token.scope
    }


def encrypt_access_token(token):
    """
    Takes a token dictionary object and returns the encrypted data.

    :param token: dictionary token object from build_token_dict()
    :return: AES encrypted string of token
    """

    data = json.dumps(token)
    cipher = Fernet(settings.FERNET_KEY)
    return cipher.encrypt(data.encode('UTF-8'))


def decrypt_access_token(enc):
    """
    Takes an encrypted string and returns a dictionary object

    :param enc: encrypted string
    :return: dictionary object
    """
    cipher = Fernet(settings.FERNET_KEY)
    data = cipher.decrypt(enc)

    return json.loads(data.decode('UTF-8'))


def create_access_token(user, scope):
    """
    Takes a user instance and return an access_token as a JsonResponse
    instance.

    :param user: django user instance
    :param scope: should be valid oauth scope value
    :return: Token dictionary object

    """

    # retrieve our oauth2 application model
    app = get_application_model().objects.get(name=settings.OAUTH2_APPLICATION_NAME)

    # Delete any existing access and refresh tokens.
    try:
        at = AccessToken.objects.get(user=user, application=app)
        RefreshToken.objects.get(user=user, access_token=at).delete()
        at.delete()
    except:
        pass

    # Generate new tokens
    atoken = generate_token()
    rtoken = generate_token()

    # Setup the access token expiration value.
    expires = now() + timedelta(seconds=oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS)

    # Create the access token model object.
    access_token = AccessToken.objects.\
        create(user=user,
               application=app,
               expires=expires,
               token=atoken,
               scope=scope)

    # Create the refresh token model object.
    RefreshToken.objects.\
        create(user=user,
               application=app,
               token=rtoken,
               access_token=access_token)

    # Return dictionary object with token information.
    return build_token_dict(access_token)


def is_access_token_valid(token):
    """
    Verify that the token information is valid and not expired
    :param token: token dictionary object
    :return: True is token is valid or False if invalid
    """

    # retrieve our oauth2 application model.
    app = get_application_model().objects.get(name=settings.OAUTH2_APPLICATION_NAME)

    # Retrieve the access token and refresh token for the user.
    try:
        at = AccessToken.objects.get(application=app, token=token['access_token'])  # Hit the db indexes.
    except:
        return False

    # Check to see if the access token has expired.
    if at.expires < now():
        return False

    return True


def get_user_from_token(token):
    """
    Return a User model record based on the token.
    :param token: token dictionary object
    :return: User Model record
    """
    # retrieve our oauth2 application model.
    app = get_application_model().objects.get(name=settings.OAUTH2_APPLICATION_NAME)

    # Retrieve the access token and refresh token for the user.
    try:
        at = AccessToken.objects.get(application=app, token=token['access_token'])  # Hit the db indexes.
    except:
        return None

    # Check to see if the access token has expired.
    if at.expires < now():
        return None

    try:
        return get_user_model().objects.get(pk=at.user_id)
    except ObjectDoesNotExist:
        pass

    return None


def refresh_access_token(token):
    """
    Refresh the access token from the refresh token, call is_access_token_valid() first.
    :param user: django user object
    :param token: token dictionary object
    :param scope: should be valid oauth scope value
    :return: token dictionary object or empty dictionary object
    """

    # retrieve our oauth2 application model.
    app = get_application_model().objects.get(name=settings.OAUTH2_APPLICATION_NAME)

    # Retrieve the access token and refresh token for the user.
    # Make sure the AT and RT are connected and not stale for some reason
    try:
        at = AccessToken.objects.get(application=app, token=token['access_token'])  # Hit the db indexes.
        rt = RefreshToken.objects.get(access_token=at, token=token['refresh_token'])  # Hit the db indexes.
    except:
        return dict()

    if not rt.user.is_active:
        return dict()

    return create_access_token(rt.user, rt.user.profile.oauth_scope)


