# -*- coding: utf-8 -*-


import asyncio
import inspect
import pytest

from base64 import b64encode as b64
from hypothesis import given
from hypothesis.strategies import text

from gitmesh.accounts import HTTPBasicAuthorizer, NoopPasswordDatabase


def _await(x, loop=None):
    loop = loop or asyncio.get_event_loop()
    print('X(1):', x)
    if inspect.iscoroutine(x) or isinstance(x, asyncio.Future):
        x = loop.run_until_complete(x)
    print('X(2):', x)
    return x


@given(username=text(min_size=1),
       password=text())
def test_noop_database(username, password):
    database = NoopPasswordDatabase()
    result = _await(database.verify_credentials(username, password))
    assert result is username


@given(password=text())
def test_noop_database_empty_username(password):
    database = NoopPasswordDatabase()
    result = _await(database.verify_credentials("", password))
    assert result is None


@pytest.mark.parametrize('token', [
    b'Authorization: Basic ' + b64(':'.join(
        ('aladin', 'opensesame')
    ).encode('utf-8')),
])
def test_http_basic(token):
    accounts = HTTPBasicAuthorizer(NoopPasswordDatabase())
    result = _await(accounts.authenticate(token))
    assert result is None


@pytest.mark.parametrize('token', [
    # No scheme.
    b'' + b64(':'.join(
        ('aladin', 'opensesame')
    ).encode('utf-8')),
    # Not basic.
    b'Digest ' + b64(':'.join(
        ('aladin', 'opensesame')
    ).encode('utf-8')),
    # Invalid Base64.
    b'Basic ' + ':'.join(
        ('aladin', 'opensesame')
    ).encode('utf-8'),
    # No colon.
    b'Basic ' + b64(''.join(
        ('aladin', 'opensesame')
    ).encode('utf-8')),
    # Empty username.
    b'Basic ' + b64(':'.join(
        ('', 'opensesame')
    ).encode('utf-8')),
])
def test_http_basic_invalid_token(token):
    accounts = HTTPBasicAuthorizer(NoopPasswordDatabase())
    result = _await(accounts.authenticate(token))
    assert result is None
