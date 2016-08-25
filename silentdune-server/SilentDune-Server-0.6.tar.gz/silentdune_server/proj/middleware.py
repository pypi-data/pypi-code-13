#
# Authors: Brett Donohoo <brett.donohoo@entpack.com>
#
# Copyright (C) 2015 EntPack
# see file 'LICENSE' for use and warranty information
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

import socket
import time
from proj.common.oauth_helper import encrypt_access_token, decrypt_access_token
from proj.common.oauth_helper import is_access_token_valid, refresh_access_token
from django.http import HttpResponseRedirect


class OAuthTokenCookieMiddleware(object):

    def process_request(self, request):

        # Check to see if this is the login/logout page, if so just return.
        if '/accounts/login/' in request.path or '/accounts/logout/' in request.path:
            return

        # TODO: Only do oauth token stuff when the url is an API url
        if 'token' in request.COOKIES:

            # Get the encrypted access token data, fix any equal sign encoding.
            enc = request.COOKIES['token'].replace('%3D', '=').encode('UTF-8')

            # Decrypt the access token data
            token = decrypt_access_token(enc)

            # Check for a valid oauth token.
            if token is not None and 'access_token' in token:

                # Check to see if access token is not valid.
                if not is_access_token_valid(token):

                    # TODO: Figure out when we should *not* just refresh the token.
                    # Try to refresh the token.
                    token = refresh_access_token(token)

                    # If we have a good refreshed token, update the cookies.
                    if 'access_token' in token:

                        # Encrypt the new token
                        enc = encrypt_access_token(token)

                        # Set the token into the request object
                        cookies = request.COOKIES.copy()
                        cookies['token'] = enc.decode('UTF-8')
                        cookies['token-update'] = "1"

                        request.COOKIES = cookies.copy()

                    else:
                        # Refresh token failed
                        return HttpResponseRedirect('/accounts/logout/')

                # Create the Authorization header with the access token.
                request.META['Authorization'] = 'bearer {0}'.format(token['access_token'])

        else:
            pass


    def process_response(self, request, response):

        # If the request object has an 'token-update' cookie, update the token cookie from the request object.
        if 'token-update' in request.COOKIES:
            response.set_cookie('token', request.COOKIES['token'])

        return response


class RequestLogMiddleware(object):
    def process_request(self, request):
        request.start_time = time.time()

    def process_response(self, request, response):

        if response['content-type'] == 'application/json':
            if getattr(response, 'streaming', False):
                response_body = '<<<Streaming>>>'
            else:
                response_body = response.content
        else:
            response_body = '<<<Not JSON>>>'

        log_data = {
            'user': request.user.pk,

            'remote_address': request.META['REMOTE_ADDR'],
            'server_hostname': socket.gethostname(),

            'request_method': request.method,
            'request_path': request.get_full_path(),
            'request_body': request.body,

            'response_status': response.status_code,
            'response_body': response_body,

            'run_time': time.time() - request.start_time,
        }

        # save log_data in some way
        #activity_logger(request, 'API' + request.method, content=request.user.pk)

        return response
