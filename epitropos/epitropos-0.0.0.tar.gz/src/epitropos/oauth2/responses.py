# -*- coding: utf-8 -*-


def client_credentials(
        access_token,
        expire_time,
        scopes=[],
        token_type='bearer'):
    """ Validates the given inputs and generates a dictionary with the
        information necessary for an OAuth2 Client Credentials flow.
    """

    _token_types = ['bearer']

    if not isinstance(scopes, list):
        raise TypeError('Scopes parameter must be a list')

    if token_type not in _token_types:
        raise ValueError('Token type %s not known. Available: %s' % (
            token_type, _token_types
        ))

    return {
        'access_token': access_token,
        'expires_in': expire_time,
        'scopes': scopes,
        'token_type': token_type,
    }
