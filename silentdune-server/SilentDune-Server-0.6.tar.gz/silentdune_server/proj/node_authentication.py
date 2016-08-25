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

import datetime

from proj.common.oauth_helper import decrypt_access_token, is_access_token_valid, get_user_from_token

from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope, OAuth2Authentication
from oauth2_provider.compat import get_user_model
from oauth2_provider.models import AccessToken
from rest_framework import authentication, permissions
from rest_framework import exceptions
from apps.node.models import Node
from django.core.exceptions import ObjectDoesNotExist


class NodeAuthentication(authentication.BaseAuthentication):
    
    def authenticate(self, request):
        """
        During Node registration, we won't have the machine_id in data, so security is handled
        by the oauth2 rest framework authentication provider. Otherwise the node needs to
        provide a node authentication header value.
        """
        if 'token' in request.COOKIES:

            # Get the encrypted access token data, fix any equal sign encoding.
            enc_token = request.COOKIES['token'].replace('%3D', '=').encode('UTF-8')
            token = decrypt_access_token(enc_token)

            # Add the HTTP_Authorization header based off the encrypted token.
            # We can only add something to the META property if we make a copy and store back the copy.
            meta = request.META.copy()
            meta['HTTP_Authorization'] = 'bearer {0}'.format(token['access_token'])
            request.META = meta

            # Retrieve the AccessToken record from the DB.
            request.auth = AccessToken.objects.get(token=token['access_token'])

            result = OAuth2Authentication().authenticate(request)
            return result

        m_id = request.META.get('HTTP_NODE')

        if not m_id:
            raise exceptions.AuthenticationFailed('Node credentials were not provided.')

        try:
            node = Node.objects.get(machine_id=m_id)
            node.last_connection = datetime.datetime.now()
            node.save()
        except:
            raise exceptions.AuthenticationFailed('Valid Node credentials were not provided.')

        return None

    def has_permission(self, request, view):
        """
        During Node registration, we won't have the machine_id in data, so security is handled
        by the oauth2 rest framework authentication provider. Otherwise the node needs to
        provide a node authentication header value.
        """
        if 'token' in request.COOKIES:

            # Get the encrypted access token data, fix any equal sign encoding.
            enc_token = request.COOKIES['token'].replace('%3D', '=').encode('UTF-8')
            token = decrypt_access_token(enc_token)

            # Add the HTTP_Authorization header based off the encrypted token.
            # We can only add something to the META property if we make a copy and store back the copy.
            meta = request.META.copy()
            meta['HTTP_Authorization'] = 'bearer {0}'.format(token['access_token'])
            request.META = meta

            # Retrieve the AccessToken record from the DB.
            request.auth = AccessToken.objects.get(token=token['access_token'])

            result = TokenHasReadWriteScope().has_permission(request, view)
            return result

        # Note: Not sure if we need to do any further permission checks on the Node here.
        return True

    def has_object_permission(self, request, view, obj):

        # Allways allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # If needed, decide if access to view and obj are allowed.
        # http://www.django-rest-framework.org/api-guide/permissions/#examples
        return True
