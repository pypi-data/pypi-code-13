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

from django.core.urlresolvers import reverse
from oauth2_provider.compat import get_user_model
from oauth2_provider.models import get_application_model

from apps.accounts.views import sdLogin
from proj.common.oauth_helper import encrypt_access_token, decrypt_access_token, is_access_token_valid, \
    refresh_access_token
from tests.base_test import BaseTest

import time

ApplicationModel = get_application_model()
UserModel = get_user_model()


# Django Oauth2 tests: https://github.com/evonove/django-oauth-toolkit/tree/master/oauth2_provider/tests


class TestOauth2Authentication(BaseTest):
    def test_is_token_valid(self):
        """ Test that the access token is valid """
        self.assertTrue(is_access_token_valid(self.token))

    def test_token_encryption(self):
        """ Test the encryption and decryption of the access token """
        enc_token = encrypt_access_token(self.token)

        self.assertTrue(enc_token)

        token = decrypt_access_token(enc_token)
        self.assertTrue(is_access_token_valid(token))
        self.assertTrue(token)

    def test_token_refresh(self):
        """ Test we can refresh the access token """
        self.assertTrue(refresh_access_token(self.token))

    def test_login_view(self):
        """
        Test the apps.accounts.views.sdLogin view. Post takes a username and password, returns a json response
        with the encrypted oauth2 token in a cookie named 'token'.
        """

        data = {
            'username': 'tester',
            'password': '12341234',
        }

        url = reverse(sdLogin)

        # Test successful login
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('token' in response.cookies)
        self.assertTrue(response.json()['status'] == 'OK')

        # Test bad login
        data = {
            'username': 'charles',
            'password': 'abc123',
        }

        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['status'] == 'ERROR')

    def test_api_node_post(self):
        """
        The url '/api/nodes' requires the oauth2 encrypted token when creating a record.
        If the 'token' cookie is not set, then the node API requires the HTTP_NODE header value
        set to access and update records.
        """

        # Encrypt the token and store it in the client cookies.
        self.client.cookies['token'] = encrypt_access_token(self.token).decode('UTF-8')

        # Set node header value and see if we can retrieve the node record.
        response = self.client.get('/api/nodes/1/', HTTP_NODE=self.machine_id)
        self.assertEquals(response.status_code, 200)

        # Check for any unmatched fields.  If there are, then check client models or node models
        # for field updates.
        data = response.json()

        # Update Node record
        data['dist_version'] = u'camelot'
        response = self.client.post('/api/nodes/', data=data)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json()['dist_version'], 'camelot')

        # Remove token cookie so we can test node authentication
        self.client.cookies.pop('token', None)

        # Test accessing the node record with no authentication set. We should get access denied.
        response = self.client.get('/api/nodes/')
        self.assertEquals(response.status_code, 403)

        # Set node header value and see if we can retrieve the node record.
        response = self.client.get('/api/nodes/1/', HTTP_NODE=self.machine_id)
        self.assertEquals(response.status_code, 200)

        # Check for any unmatched fields.  If there are, then check client models or node models
        # for field updates.
        unmatched = set(response.json()) ^ set(data)
        self.assertTrue(len(unmatched) == 0)


