# -*- coding: utf-8 -*-


def invalid_scope(error_description=None):
    """ The requested scope is invalid, unknown, malformed, or exceeds the
        scope granted by the resource owner.
    """

    if not error_description:
        error_description = 'Invalid, unknown, or malformed scope request.'

    return {
        'error': 'invalid_scope',
        'error_description': error_description,
    }


def unsupported_grant_type(error_description=None):
    """ The requested authorization grant type is not supported by the
        authorization server.
    """

    if not error_description:
        error_description = 'Unsupported or invalid grant type.'

    return {
        'error': 'unsupported_grant_type',
        'error_description': error_description,
    }


def unauthorized_client(error_description=None):
    """ The authenticated client is not authorized to use the requested
        grant type.
    """

    if not error_description:
        error_description = 'Not authorized to use requested grant type.'

    return {
        'error': 'unauthorized_client',
        'error_description': error_description,
    }


def invalid_grant(error_description=None):
    """ The provided authorization grant (eg., auth token, resource owner
        credentials) or refresh token is invalid, expired, revoked, or does
        not match the redirection URI used in the authorization request,
        or was issued to another client.
    """

    if not error_description:
        error_description = 'Authorization or refresh token invalid.'

    return {
        'error': 'invalid_grant',
        'error_description': error_description,
    }


def invalid_client(error_description=None):
    """ Client authentication failed (e.g., unknown client, no client
        authentication included, or unsupported authentication method).
    """

    if not error_description:
        error_description = 'Client authentication failed.'

    return {
        'error': 'invalid_client',
        'error_description': error_description,
    }


def invalid_request(error_description=None):
    """ Request is missing a required parameter, includes an unsupported
        parameter value (other than grant type), repeats a parameter,
        includes multiple credentials, utilizes more than one mechanism
        for authenticating the client, or is otherwise malformed.
    """

    if not error_description:
        error_description = 'Invalid or malformed request.'

    return {
        'error': 'invalid_request',
        'error_description': error_description,
    }
