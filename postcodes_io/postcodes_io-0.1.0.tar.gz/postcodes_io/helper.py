import json
import functools
import requests

try:
    # py3.5
    import http
    HTTPStatus = http.HTTPStatus

except AttributeError:
    # py3
    import http.client
    HTTPStatus = http.client

except ImportError:
    # py2
    import httplib
    HTTPStatus = httplib

from .exceptions import PostcodeError, PostcodeNotFoundError


def json_response(fn):
    """
    decorator to transform Http response into JSON

    :param fn: method being decorated
    :return: wrapped function
    """
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):

        resp = fn(*args, **kwargs)
        text = json.loads(resp.text)

        if resp.status_code == HTTPStatus.OK:
            return text['result']

        elif resp.status_code == HTTPStatus.NOT_FOUND:
            raise PostcodeNotFoundError(text['error'])

        elif resp.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
            raise PostcodeError(text['error'])

        return resp

    return wrapper

# wrap requests.get() and post() to return JSON
http_get = json_response(requests.get)
http_post = json_response(requests.post)
