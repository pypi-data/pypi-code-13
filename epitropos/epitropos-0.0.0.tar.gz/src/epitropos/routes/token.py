# -*- coding: utf-8 -*-
from __future__ import print_function

import base64
import time

from bottle import (
    request
)
from epitropos import plugin
from epitropos.oauth2 import (
    errors,
    responses
)
from epitropos.util import generate_random_token
from malibu.command.module import CommandModuleLoader
from malibu.util.log import LoggingDriver
from restify import routing
from restify.routing.base import (
    api_route,
    json_response,
    status_returned
)
from urllib import unquote_plus
from urlparse import parse_qs


@routing.routing_module
class TokenAPIRouter(routing.base.APIRouter):
    """ Router for generation and validity checking endpoints.

        POST /token
        POST /token/check
        POST /token/revoke
    """

    def __init__(self, manager):

        super(TokenAPIRouter, self).__init__(manager)

        self._log = LoggingDriver.find_logger()

        cfg = (
            CommandModuleLoader(None, state='epitropos')
            .get_module_by_base('config')
            .get_configuration())

        auth_cfg = cfg.get_namespace('auth')
        auth_gen = auth_cfg.get('general', {})

        self._settings = {
            'token_length': auth_gen.get_int('token_length', 32),
            'token_expiry': auth_gen.get_int('expires_after', 3600),
        }

        self.auth_plugin = plugin.authentication()
        self.store_plugin = plugin.storage()

    @api_route(
        path='/token',
        actions=['POST'],
        returns='application/json'
    )
    @json_response
    @status_returned
    def token_post(self):
        """ POST /token

            Performs authentication and returns a token if credentials
            are able to be verified.

            Credentials should be passed through the HTTP Authorization header
            in HTTP BASIC form, a process like this:

                username = someuser
                password = somesecret

                authstr = username + ':' + password
                b64str = base64.encodestring(authstr)
                headerval = "Basic %s" % (b64str)

            The accepted Content-Type is application/x-www-form-urlencoded.
            A maximum of two urlencoded variables will be accept:
             - scope            [ optional ]
             - grant_type       [ required ]

            Note that the space-delimited scopes *SHOULD* get quoted into
            plus-delimited scopes, as that is the proper way to handle spaces
            when there is the potentiality of having a quoted URL inside a
            URL-encoded data-string. This handles the case where many places
            define scopes as a URL which defines the actual scope.

            For example, Google has a set of scopes which are almost identical
            with some handling additional cases:

                `profile` -vs- `https://www.googleapis.com/auth/plus.login`

            The full request will look like this:

                POST /token HTTP/1.1
                Host: auth.example.org
                Authorization: Basic c29tZXVzZXJuYW1lOnNvbWVwYXNzd29yZCE=
                Content-Type: application/x-www-form-urlencoded

                grant_type=client_credentials&scope=space+delim+scopes
        """

        # Process the Authorization header
        auth_data = request.get_header('Authorization', None)
        if not auth_data:
            resp = self.generate_error_response(code=400)
            resp.update(errors.invalid_request(
                error_description='Missing `Authorization` header'
            ))

            return resp

        auth_hdr = auth_data.split()
        if auth_hdr[0] != 'Basic':
            resp = self.generate_error_response(code=400)
            resp.update(errors.invalid_request(
                error_description='Invalid `Authorization` type: %s' % (
                    auth_hdr[0]
                )
            ))

            return resp

        auth_str = base64.b64decode(auth_hdr[1])
        username, password = auth_str.split(':', 1)
        if not username or not password:
            resp = self.generate_error_response(code=400)
            resp.update(errors.invalid_request(
                error_description='`Authorization` header missing username '
                                  'or password'
            ))

            return resp

        # Check Content-Type header and process request body.
        content_type = request.get_header('Content-Type', None)
        if content_type != 'application/x-www-form-urlencoded':
            resp = self.generate_error_response(code=406)
            resp.update(errors.invalid_request(
                error_description='`Content-Type` given is unacceptible'
            ))

            return resp

        try:
            req_info = parse_qs(unquote_plus(request.body.read()))
        except Exception as e:
            resp = self.generate_error_response(
                code=400,
                exception=e
            )
            resp.update(errors.invalid_request(
                error_description='Malformed POST data'
            ))

            return resp

        grant_type = req_info.get('grant_type', None)
        if not grant_type:
            resp = self.generate_error_response(code=400)
            resp.update(errors.invalid_request(
                error_description='Missing or malformed `grant_type`'
            ))

            return resp

        scopes = req_info.get('scope', None)
        if not scopes:
            resp = self.generate_error_response(code=400)
            resp.update(errors.invalid_request(
                error_description='Missing or malformed `scope`'
            ))

            return resp

        try:
            grant_type = grant_type[0]
            req_scopes = frozenset(scopes[0].split())
        except Exception as e:
            resp = self.generate_error_response(
                code=500,
                exception=e
            )
            resp.update(errors.invalid_request(
                error_description='Error while processing POST data'
            ))

            return resp

        if grant_type == 'client_credentials':
            # Perform authentication.
            auth_res = self.auth_plugin.authenticate(username, password)
            if not auth_res:
                # Authentication failed :(
                resp = self.generate_error_response(code=403)
                resp.update(errors.unauthorized_client(
                    error_description='Authentication failed'
                ))

                return resp

            # Check user's scope access
            has_scopes = self.auth_plugin.scopes(username)
            if req_scopes & has_scopes == req_scopes:
                # Backend users has access to all scopes requested
                pass
            else:
                # There is a subset of scopes that the user does not have
                bad_scope = req_scopes - has_scopes
                resp = self.generate_error_response(code=403)
                resp.update(errors.invalid_scope(
                    error_description='User has no scope(s): %s' % (bad_scope)
                ))

                return resp

            # Authentication success! Create a token.
            creation_time = time.time()
            expire_time = creation_time + self._settings.get(
                'token_expiry',
                3600
            )

            auth_token = generate_random_token(
                length=self._settings.get('token_length', 32)
            )

            session = {
                'created_at': creation_time,
                'expires_at': expire_time,
                'scopes': ' '.join(req_scopes),
                'token': auth_token,
                'username': username,
            }

            store_key = 'auth-token:' + auth_token

            self.store_plugin.insert(store_key, session)

            resp = self.generate_bare_response()
            resp.update(responses.client_credentials(
                auth_token,
                self._settings.get('token_expiry', 3600),
                scopes=list(req_scopes),
                token_type='bearer'
            ))

            return resp
        else:
            resp = self.generate_error_response(code=501)
            resp.update(errors.unsupported_grant_type(
                error_description='Requested grant type is not available'
            ))

            return resp

        resp = self.generate_error_response(code=500)
        resp.update(errors.invalid_request(
            error_description='Unknown request or processing error'
        ))

        return resp

    @api_route(
        path='/token/check',
        actions=['POST'],
        returns='application/json'
    )
    @json_response
    @status_returned
    def token_check_post(self):
        """ POST /token/check

            Given a token, username, and list of scopes, returns either
            200 OK if the token is associated with the given username and has
            at least the list of scopes, or 401 Unauthorized otherwise.

            The scopes given can only be a subset of the scopes the token was
            created with. This means that:

                Given: {"admin", "user", "rw"}
                       {"admin", "user", "rw"} is a subset
                       {"admin", "user"}       is a subset
                       {"user"}                is a subset
                       {}                      is a subset
                       ...                     so on and so forth.

            The full request will look like this:

                POST /token/check HTTP/1.1
                Host: auth.example.org
                Content-Type: application/x-www-form-urlencoded

                access_token=...&username=...&scope=space+delim+scopes

        """

        # Check Content-Type header and process request body.
        content_type = request.get_header('Content-Type', None)
        if content_type != 'application/x-www-form-urlencoded':
            resp = self.generate_error_response(code=406)
            resp.update(errors.invalid_request(
                error_description='`Content-Type` given is unacceptible'
            ))

            return resp

        try:
            req_info = parse_qs(unquote_plus(request.body.read()))
        except Exception as e:
            resp = self.generate_error_response(
                code=400,
                exception=e
            )
            resp.update(errors.invalid_request(
                error_description='Malformed POST data'
            ))

            return resp

        authtok = req_info.get('access_token', [None])[0]
        if not authtok:  # *REQUIRED* parameter
            resp = self.generate_error_response(code=400)
            resp.update(errors.invalid_request(
                error_description='Missing or malformed `access_token`'
            ))

            return resp

        username = req_info.get('username', [None])[0]
        if not username:  # *REQUIRED* parameter
            resp = self.generate_error_response(code=400)
            resp.update(errors.invalid_request(
                error_description='Missing or malformed `username`'
            ))

            return resp

        scopes = req_info.get('scope', [None])[0]
        if not scopes:  # *OPTIONAL* parameter
            scopes = set()
        else:
            scopes = set(scopes.split())

        # Try to fetch the token info from the store.
        token_info = self.store_plugin.find(key='auth-token:' + authtok)
        if not token_info:
            # Token is not in the backend
            resp = self.generate_error_response(code=401)
            resp.update(errors.unauthorized_client(
                error_description='Unknown username or token.'
            ))

            return resp

        tok_username = token_info.get('username')
        if not tok_username or tok_username != username:
            # Username mismatch
            resp = self.generate_error_response(code=401)
            resp.update(errors.unauthorized_client(
                error_description='Invalid username or token.'
            ))

            return resp

        # The scopes here are a touchy subject.. We want the scopes in the
        # access request to be a subset of the granted scopes, but the access
        # request may not have given scopes.
        tok_scopes = set(token_info.get('scopes', '').split())
        if not scopes.issubset(tok_scopes):
            # Ungranted scopes
            ungranted = scopes - tok_scopes
            resp = self.generate_error_response(code=401)
            resp.update(errors.invalid_scope(
                error_description='Ungranted scopes: ' + ', '.join(ungranted)
            ))

            return resp

        resp = self.generate_bare_response()
        return resp

    @api_route(
        path='/token/revoke',
        actions=['POST'],
        returns='application/json'
    )
    @json_response
    @status_returned
    def token_revoke_post(self):
        """ POST /token/revoke

            Given a token, checks the storage backend for the token and, if
            present, revokes it. If the token does not exist, no action is
            taken.

            Only returns 4xx codes if a processing error occurs. 202 will be
            returned regardless of the presence of the token in the backend.

            The full request will look like this:

                POST /token/revoke HTTP/1.1
                Host: auth.example.org
                Content-Type: application/x-www-form-urlencoded

                access_token=...token...

        """

        # Check Content-Type header and process request body.
        content_type = request.get_header('Content-Type', None)
        if content_type != 'application/x-www-form-urlencoded':
            resp = self.generate_error_response(code=406)
            resp.update(errors.invalid_request(
                error_description='`Content-Type` given is unacceptible'
            ))

            return resp

        try:
            req_info = parse_qs(unquote_plus(request.body.read()))
        except Exception as e:
            resp = self.generate_error_response(
                code=400,
                exception=e
            )
            resp.update(errors.invalid_request(
                error_description='Malformed POST data'
            ))

            return resp

        authtok = req_info.get('access_token', [None])[0]
        if not authtok:  # *REQUIRED* parameter
            resp = self.generate_error_response(code=400)
            resp.update(errors.invalid_request(
                error_description='Missing or malformed `access_token`'
            ))

            return resp

        # Try to fetch the token info from the store.
        token_info = self.store_plugin.find(key='auth-token:' + authtok)
        if not token_info:
            # Token is not in the backend
            resp = self.generate_bare_response()
            resp.update({
                'status': 202,
            })

            return resp

        self.store_plugin.remove(key='auth-token:' + authtok)

        resp = self.generate_bare_response()
        resp.update({
            'status': 204,
        })

       return resp
