# -*- coding: utf-8 -*-


import base64


class Accounts(object):
    """Autorization protocol."""

    async def authenticate(self, token):
        """Extract and verify credentials from HTTP autorization header.

        :param token: The contents of the HTTP authorization header (may be
         empty or ``None``).
        :return: The username if credentials are valid, else ``None``.

        """
        raise NotImplementedError


class PasswordDatabase(object):
    """Username & password autorization protocol."""

    async def verify_credentials(self, username, password):
        raise NotImplementedError


class NoopPasswordDatabase(PasswordDatabase):

    async def verify_credentials(self, username, password):
        if not username:
            return None
        return username


class HTTPBasicAuthorizer(object):
    """Verifies HTTP basic token against a password database."""

    def __init__(self, password_database):
        """Prepare the authorizer.

        :param password_database: Database against which to verify (username,
         password) pairs extracted from the HTTP authorization header.

        """

        self._password_database = password_database

    async def authenticate(self, token):
        """."""

        token = token.strip().split(b' ', 1)
        if len(token) != 2:
            return None
        scheme, token = token
        if scheme.lower() != b'basic':
            return None
        try:
            token = base64.b64decode(token)
        except TypeError:
            return None
        token = token.split(b':', 1)
        if len(token) != 2:
            return None
        username, password = token
        if not username:
            return None
        return await self._password_database.verify_credentials(
            username, password
        )
