# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2014, 2015, 2016 CERN.
#
# Invenio is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

"""Test case for views."""

from __future__ import absolute_import

import time

import pytest
from flask import url_for
from flask_login import _create_identifier, login_user
from flask_oauthlib.client import OAuth as FlaskOAuth
from invenio_db import db
from itsdangerous import TimedJSONWebSignatureSerializer
from mock import MagicMock, patch
from simplejson import JSONDecodeError
from six.moves.urllib_parse import parse_qs, urlparse

from invenio_oauthclient import InvenioOAuthClient
from invenio_oauthclient.handlers import token_getter
from invenio_oauthclient.models import RemoteAccount, RemoteToken
from invenio_oauthclient.views.client import blueprint as blueprint_client
from invenio_oauthclient.views.client import serializer
from invenio_oauthclient.views.settings import blueprint as blueprint_settings


def mock_response(oauth, remote_app='test', data=None):
    """Mock the oauth response to use the remote."""
    # Mock oauth remote application
    oauth.remote_apps[remote_app].handle_oauth2_response = MagicMock(
        return_value=data or {
            "access_token": "test_access_token",
            "scope": "",
            "token_type": "bearer"
        }
    )


def test_redirect_uri(views_fixture):
    """Test redirect uri."""
    app = views_fixture
    with app.test_client() as client:
        # Test redirect
        resp = client.get(
            url_for("invenio_oauthclient.login", remote_app='test',
                    next='http://inveniosoftware.org')
        )
        assert resp.status_code == 302

        # Verify parameters
        params = parse_qs(urlparse(resp.location).query)
        assert params['response_type'] == ['code']
        assert params['client_id'] == ['testid']
        assert params['redirect_uri']
        assert params['state']

        # Verify next parameter in state token does not allow blanco redirects
        state = serializer.loads(params['state'][0])
        assert state['next'] is None

        # Assert redirect uri does not have any parameters.
        params = parse_qs(urlparse(params['redirect_uri'][0]).query)
        assert params == {}

        # Assert that local redirects are allowed
        test_urls = [
            '/search',
            url_for('invenio_oauthclient.disconnect', remote_app='test',
                    _external=True)
        ]
        for url in test_urls:
            resp = client.get(
                url_for("invenio_oauthclient.login", remote_app='test',
                        next=url)
            )
            assert resp.status_code == 302
            state = serializer.loads(
                parse_qs(urlparse(resp.location).query)['state'][0]
            )
            assert url == state['next']


def test_login(views_fixture):
    """Test login."""
    app = views_fixture
    with app.test_client() as client:
        # Test redirect
        resp = client.get(
            url_for("invenio_oauthclient.login", remote_app='test', next='/')
        )
        assert resp.status_code == 302

        params = parse_qs(urlparse(resp.location).query)
        assert params['response_type'] == ['code']
        assert params['client_id'] == ['testid']
        assert params['redirect_uri']
        assert params['state']

        # Invalid remote
        resp = client.get(
            url_for("invenio_oauthclient.login", remote_app='invalid')
        )
        assert resp.status_code == 404


def test_authorized(base_app, params):
    """Test login."""
    app = base_app

    handled = {}

    def test_authorized_handler(resp, remote, *args, **kwargs):
        """Save configuration."""
        handled['resp'] = resp
        handled['remote'] = remote
        handled['args'] = args
        handled['kwargs'] = kwargs
        return "TEST"

    def test_invalid_authorized_handler(resp, remote, *args, **kwargs):
        """Set wrong configuration."""
        handled['resp'] = 1
        handled['remote'] = 1
        handled['args'] = 1
        handled['kwargs'] = 1

    base_app.config['OAUTHCLIENT_REMOTE_APPS'].update(
        dict(
            test=dict(
                authorized_handler=test_authorized_handler,
                params=params('testid'),
                title='MyLinkedTestAccount',
            ),
            test_invalid=dict(
                authorized_handler=test_invalid_authorized_handler,
                params=params('test_invalidid'),
                title='Test Invalid',
            ),
            full=dict(
                params=params("fullid"),
                title='Full',
            ),
        )
    )

    FlaskOAuth(app)
    InvenioOAuthClient(app)
    base_app.register_blueprint(blueprint_client)
    base_app.register_blueprint(blueprint_settings)

    with app.test_client() as client:
        # Ensure remote apps have been loaded (due to before first
        # request)
        client.get(url_for("invenio_oauthclient.login", remote_app='test'))
        mock_response(app.extensions['oauthlib.client'], 'test')
        mock_response(app.extensions['oauthlib.client'], 'test_invalid')

        from invenio_oauthclient.views.client import serializer

        state = serializer.dumps({
            'app': 'test',
            'sid': _create_identifier(),
            'next': None,
        })

        resp = client.get(
            url_for(
                "invenio_oauthclient.authorized",
                remote_app='test',
                code='test',
                state=state
            )
        )
        assert resp.data == b"TEST"
        assert handled['remote'].name == 'test'
        assert not handled['args']
        assert not handled['kwargs']
        assert handled['resp']['access_token'] == 'test_access_token'

        state = serializer.dumps({
            'app': 'test_invalid',
            'sid': _create_identifier(),
            'next': None,
        })

        # handler should be return something
        with pytest.raises(ValueError):
            client.get(url_for(
                "invenio_oauthclient.authorized",
                remote_app='test_invalid',
                code='test',
                state=state,
            ))


def test_invalid_authorized_response(views_fixture):
    """Test login."""
    app = views_fixture
    oauth = app.extensions['oauthlib.client']
    with app.test_client() as client:
        # Fake an authorized request
        # Ensure remote apps have been loaded (due to before first
        # request)
        client.get(url_for("invenio_oauthclient.login", remote_app='test'))

        oauth.remote_apps['test'].handle_oauth2_response = MagicMock(
            side_effect=JSONDecodeError('Expecting value', '', 0)
        )

        state = serializer.dumps({
            'app': 'test',
            'sid': _create_identifier(),
            'next': None,
        })

        with pytest.raises(JSONDecodeError):
            client.get(url_for(
                "invenio_oauthclient.authorized",
                remote_app='test',
                code='test',
                state=state
            ))


def test_state_token(views_fixture, monkeypatch):
    """Test state token."""
    # Mock session id
    monkeypatch.setattr('flask_login._create_identifier', lambda: '1234')
    monkeypatch.setattr(
        'invenio_oauthclient.views.client._create_identifier', lambda: '1234')
    app = views_fixture

    with app.test_client() as client:
        # Ensure remote apps have been loaded (due to before first
        # request)
        client.get(url_for("invenio_oauthclient.login", remote_app='test'))
        mock_response(app.extensions['oauthlib.client'], 'test')

        # Good state token
        state = serializer.dumps(
            {'app': 'test', 'sid': '1234',  'next': None, }
        )
        resp = client.get(
            url_for("invenio_oauthclient.authorized", remote_app='test',
                    code='test', state=state)
        )
        assert resp.status_code == 200

        outdated_serializer = TimedJSONWebSignatureSerializer(
            app.config['SECRET_KEY'],
            expires_in=0,
        )

        # Bad state - timeout
        state1 = outdated_serializer.dumps(
            {'app': 'test', 'sid': '1234',  'next': None, }
        )
        # Bad state - app
        state2 = serializer.dumps(
            # State for another existing app (test_invalid exists)
            {'app': 'test_invalid', 'sid': '1234',  'next': None, }
        )
        # Bad state - sid
        state3 = serializer.dumps(
            # State for another existing app (test_invalid exists)
            {'app': 'test', 'sid': 'bad',  'next': None, }
        )
        time.sleep(1)
        for s in [state1, state2, state3]:
            resp = client.get(
                url_for("invenio_oauthclient.authorized", remote_app='test',
                        code='test', state=s)
            )
            assert resp.status_code == 403


def test_no_remote_app(views_fixture):
    """Test no remote app."""
    app = views_fixture
    with app.test_client() as client:
        resp = client.get(
            url_for("invenio_oauthclient.authorized", remote_app='invalid')
        )
        assert resp.status_code == 404

        resp = client.get(
            url_for("invenio_oauthclient.disconnect", remote_app='invalid')
        )
        assert resp.status_code == 404


def test_token_getter_setter(views_fixture, monkeypatch):
    """Test token getter setter."""
    # Mock session id
    monkeypatch.setattr('flask_login._create_identifier', lambda: '1234')
    monkeypatch.setattr(
        'invenio_oauthclient.views.client._create_identifier', lambda: '1234')

    app = views_fixture
    oauth = app.extensions['oauthlib.client']

    # Mock user
    user = MagicMock()
    user.id = 1
    user.get_id = MagicMock(return_value=1)
    user.is_anonymous = False

    with patch('flask_login._get_user', return_value=user):
        with app.test_client() as c:
            # First call login to be redirected
            res = c.get(url_for("invenio_oauthclient.login",
                                remote_app='full'))
            assert res.status_code == 302
            assert res.location.startswith(
                oauth.remote_apps['full'].authorize_url
            )
            state = parse_qs(urlparse(res.location).query)['state'][0]

            # Mock resposen class
            mock_response(app.extensions['oauthlib.client'], 'full')

            # Imitate that the user authorized our request in the remote
            # application.
            c.get(url_for(
                "invenio_oauthclient.authorized", remote_app='full',
                code='test', state=state,
            ))

            # Assert if everything is as it should be.
            from flask import session as flask_session
            assert flask_session['oauth_token_full'] == \
                ('test_access_token', '')

            t = RemoteToken.get(1, "fullid")
            assert t.remote_account.client_id == 'fullid'
            assert t.access_token == 'test_access_token'
            assert RemoteToken.query.count() == 1

            # Mock a new authorized request
            mock_response(app.extensions['oauthlib.client'], 'full', data={
                "access_token": "new_access_token",
                "scope": "",
                "token_type": "bearer"
            })

            c.get(url_for(
                "invenio_oauthclient.authorized", remote_app='full',
                code='test', state=state
            ))

            t = RemoteToken.get(1, "fullid")
            assert t.access_token == 'new_access_token'
            assert RemoteToken.query.count() == 1

            val = token_getter(
                app.extensions['oauthlib.client'].remote_apps['full'])
            assert val == ('new_access_token', '')

            # Disconnect account
            res = c.get(url_for(
                "invenio_oauthclient.disconnect", remote_app='full',
            ))
            assert res.status_code == 302
            assert res.location.endswith(
                url_for('invenio_oauthclient_settings.index')
            )
            # Assert that remote account have been removed.
            t = RemoteToken.get(1, "fullid")
            assert t is None
            # TODO: Figure out what is leaving session open & blocked
            db.session.close()


def test_rejected(views_fixture, monkeypatch):
    """Test rejected."""
    # Mock session id
    monkeypatch.setattr('flask_login._create_identifier', lambda: '1234')
    monkeypatch.setattr(
        'invenio_oauthclient.views.client._create_identifier', lambda: '1234')

    app = views_fixture
    oauth = app.extensions['oauthlib.client']

    # Mock user id
    user = MagicMock()
    user.get_id = MagicMock(return_value=1)
    user.is_authenticated = MagicMock(return_value=True)

    with patch('flask_login._get_user', return_value=user):
        with app.test_client() as c:
            # First call login to be redirected
            res = c.get(url_for("invenio_oauthclient.login",
                                remote_app='full'))
            assert res.status_code == 302
            assert res.location.startswith(
                oauth.remote_apps['full'].authorize_url
            )

            # Mock response to imitate an invalid response. Here, an
            # example from GitHub when the code is expired.
            mock_response(app.extensions['oauthlib.client'], 'full', data=dict(
                error_uri='http://developer.github.com/v3/oauth/'
                '#bad-verification-code',
                error_description='The code passed is '
                'incorrect or expired.',
                error='bad_verification_code',
            ))

            # Imitate that the user authorized our request in the remote
            # application (however, the remote app will son reply with an
            # error)
            state = serializer.dumps({
                'app': 'full', 'sid': '1234',  'next': None,
            })

            res = c.get(url_for(
                "invenio_oauthclient.authorized", remote_app='full',
                code='test', state=state
            ))
            assert res.status_code == 302


def test_settings_view(views_fixture):
    """Test settings view."""
    app = views_fixture
    app.login_manager.login_view = None
    login_manager = app.login_manager
    datastore = app.extensions['invenio-accounts'].datastore

    @login_manager.user_loader
    def load_user(user_id):
        return user

    @app.route('/foo_login')
    def login():
        user = datastore.find_user(email="existing@inveniosoftware.org")
        login_user(user)
        return "Logged In"

    with app.app_context():
        with app.test_client() as client:
            user = datastore.find_user(email="existing@inveniosoftware.org")
            RemoteAccount.create(user.get_id(), 'testid', None)

            resp = client.get(url_for('invenio_oauthclient_settings.index'),
                              follow_redirects=False)
            assert resp.status_code == 401

            # make a fake login (using my login function)
            client.get('/foo_login', follow_redirects=True)

            resp = client.get(url_for('invenio_oauthclient_settings.index'),
                              follow_redirects=True)
            assert resp.status_code == 200
            assert b'MyLinkedTestAccount' in resp.data
            assert url_for('invenio_oauthclient.disconnect',
                           remote_app='test') in resp.data.decode("utf-8")
            assert url_for('invenio_oauthclient.login',
                           remote_app='full') in resp.data.decode("utf-8")
            assert url_for(
                'invenio_oauthclient.login',
                remote_app='test_invalid') in resp.data.decode("utf-8")
