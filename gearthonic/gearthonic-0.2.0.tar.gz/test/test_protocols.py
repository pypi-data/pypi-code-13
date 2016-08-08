"""Tests for the protocols."""
from _ssl import CERT_REQUIRED, CERT_NONE

import pytest
from mock import Mock, patch

from gearthonic.exceptions import ConfigurationError
from gearthonic.protocols import XmlRpcProtocol, JsonRpcProtocol


class TestXmlProtocol(object):
    """Tests for the XML RPC protocol."""

    @patch('gearthonic.protocols.ServerProxy')
    def test_server_proxy_configuration(self, server_mock):
        XmlRpcProtocol('example.com', 1234)
        server_mock.assert_called()
        args, kwargs = server_mock.call_args_list[0]
        assert args[0] == 'https://example.com:1234'
        assert kwargs['context'].verify_mode == CERT_REQUIRED

    @patch('gearthonic.protocols.ServerProxy')
    def test_insecure_server_proxy_configuration(self, server_mock):
        XmlRpcProtocol('example.com', 1234, secure=False)
        server_mock.assert_called_once_with('http://example.com:1234', context=None)
        server_mock.reset_mock()

        XmlRpcProtocol('example.com', 1234, verify=False)
        server_mock.assert_called()
        args, kwargs = server_mock.call_args_list[0]
        assert args[0] == 'https://example.com:1234'
        assert kwargs['context'].verify_mode == CERT_NONE

    @patch('gearthonic.protocols.ServerProxy')
    def test_authentication(self, server_mock):
        XmlRpcProtocol('example.com', 1234, username='ham', password='eggs')
        server_mock.assert_called()
        args, kwargs = server_mock.call_args_list[0]
        assert args[0] == 'https://ham:eggs@example.com:1234'

    def test_authentication_with_insecure_connection(self):
        with pytest.raises(ConfigurationError):
            XmlRpcProtocol('example.com', 1234, secure=False, username='ham', password='eggs')

    @patch('gearthonic.protocols.ServerProxy', new=Mock())
    def test_call_method(self):
        xrp = XmlRpcProtocol('example.com', 1234)
        xrp.call('listMethods', 'foobar', ham='eggs')
        xrp.proxy.listMethods.assert_called()
        xrp.proxy.listMethods.assert_called_once_with('foobar', ham='eggs')


class TestJsonProtocol(object):
    """Tests for the JSON RPC protocol."""

    def test_http_connection_configuration(self):
        jrp = JsonRpcProtocol('example.com', 1234)
        assert jrp.uri == 'https://example.com:1234'
        assert jrp.server.endpoint == 'https://example.com:1234'
        assert jrp.server.session.verify
        assert not jrp.authentication

    def test_insecure_http_connection_configuration(self):
        jrp = JsonRpcProtocol('example.com', 1234, secure=False)
        assert jrp.uri == 'http://example.com:1234'
        assert jrp.server.endpoint == 'http://example.com:1234'
        assert jrp.server.session.verify
        assert not jrp.authentication

        jrp = JsonRpcProtocol('example.com', 1234, verify=False)
        assert jrp.uri == 'https://example.com:1234'
        assert jrp.server.endpoint == 'https://example.com:1234'
        assert not jrp.server.session.verify
        assert not jrp.authentication

    def test_authentication_configuration(self):
        jrp = JsonRpcProtocol('example.com', 1234, username='ham', password='eggs')
        assert jrp.uri == 'https://example.com:1234'
        assert jrp.server.endpoint == 'https://example.com:1234'
        assert jrp.server.session.verify
        assert jrp.authentication
        assert jrp.server.session.auth == ('ham', 'eggs')

    def test_authentication_with_insecure_connection(self):
        with pytest.raises(ConfigurationError):
            JsonRpcProtocol('example.com', 1234, secure=False, username='ham', password='eggs')
