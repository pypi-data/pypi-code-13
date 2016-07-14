from axsemantics import constants
from axsemantics.errors import (
    APIError,
    AuthenticationError,
)
from axsemantics.net import RequestHandler


def login(user, password):
    error = None
    try:
        login_myax(user, password)
    except AuthenticationError as e:
        print('WARNING: data api authentication failed')
        error = e
    try:
        login_rincewind(user, password)
    except AuthenticationError as e:
        if error:
            # only raise if both failed
            raise
        else:
            print('WARNING: training api authentication failed')



def login_myax(user, password, api_base=None):
    if api_base is None:
        api_base = constants.API_BASE

    data = {
        'email': user,
        'password': password,
    }

    requestor = RequestHandler(api_base=api_base)

    try:
        response = requestor.request(
            url='/{}/rest-auth/login/'.format(constants.API_VERSION),
            method='post',
            params=data,
        )
    except APIError as error:
        if hasattr(error, 'request') and error.request.status_code == 400:
            raise AuthenticationError(error.request) from None
        else:
            raise

    if constants.DEBUG:
        print('Received Myax authentication token {}.'.format(response['key']))
    constants.API_TOKEN = response['key']


def login_rincewind(user, password, api_base=None):
    if api_base is None:
        api_base = constants.API_BASE_RINCEWIND

    data = {
        'username': user,
        'password': password,
    }

    requestor = RequestHandler(api_base=api_base)

    try:
        response = requestor.request(
            url='/get-auth-token/',
            method='post',
            params=data,
        )
    except APIError as error:
        if hasattr(error, 'request') and error.request.status_code == 400:
            raise AuthenticationError(error.request) from None
        else:
            raise

    if constants.DEBUG:
        print('Received Rincewind authentication token {}.'.format(response['token']))
    constants.API_TOKEN = response['token']


def create_object(data, api_token=None, _type=None, **kwargs):
    from axsemantics.resources import (
        ContentProject,
        Thing,
        Training,
    )
    types = {
        'content-project': ContentProject,
        'thing': Thing,
        'training': Training,
    }

    if isinstance(data, list):
        return [create_object(element, api_token, type=_type, **kwargs) for element in data]

    from axsemantics.base import AXSemanticsObject
    if isinstance(data, dict) and not isinstance(data, AXSemanticsObject):
        data = data.copy()

        _class = types.get(_type, AXSemanticsObject)
        return _class.create_from_dict(data, api_token, **kwargs)

    return data


def _get_update_dict(current, previous):
    if isinstance(current, dict):
        previous = previous or {}
        diff = current.copy()
        diff.update({
            key: ''
            for key in set(previous.keys()) - set(current.keys())
        })
        return diff

    return current if current is not None else ""
