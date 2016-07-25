# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from io import BytesIO
import poort as p
from utils import get_environ
import disinfect as d
from pytest import raises


class TestRequest(object):
    def test_copy_request_environ(self):
        environ = get_environ('multipart-post')
        assert isinstance(environ['wsgi.input'], BytesIO)

        environ['gunicorn.socket'] = True
        assert 'wsgi.errors' in environ

        copy = p.utils.copy_request_environ(environ)

        assert 'wsgi.errors' not in copy
        assert copy['INPUT'] == environ['wsgi.input'].read()

    def test_without_gunicorn(self):
        environ = get_environ('multipart-post')

        assert 'gunicorn.socket' not in environ

        copy = p.utils.copy_request_environ(environ)

        assert 'wsgi.errors' not in copy
        assert copy['INPUT'] == environ['wsgi.input'].read()

    def test_disinfect_or_json_400(self):
        mapping = d.Mapping({
            'first': d.String(),
        })

        with raises(p.TerminatingResponse) as exc:
            p.disinfect_or_json_400({
                'last': 'Corver'
            }, mapping)

        assert exc.value.response
        assert isinstance(exc.value.response, p.JsonResponse)

        data = exc.value.response.data

        assert data['message'] == 'Validation error.'
        assert data['errors']['first'] == 'Field is required.'
