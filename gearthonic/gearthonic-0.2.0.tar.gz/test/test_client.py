"""Tests for `gearthonic` module."""

from mock import Mock
from gearthonic import client


class TestGearClient(object):
    """Tests for the base GearClient"""

    def test_getttr_function(self, gear_client):
        """Test that __getattr__ returns a callable"""
        fnc = gear_client.ham
        assert callable(fnc)

    def test_magic_call(self, gear_client):
        """Test that any call gets redirected to the ``call`` method of the GearClient."""
        gear_client.call = Mock()
        gear_client.list_all(1, ham='eggs')

        assert gear_client.call.called
        gear_client.call.assert_called_once_with('list_all', 1, ham='eggs')

    def test_call_method(self, gear_client):
        """Test that the call method redirects any call to the XML RPC ServerProxy."""
        gear_client.protocol = Mock()
        gear_client.call('list_all', 1, ham='eggs')

        assert gear_client.protocol.call.called
        gear_client.protocol.call.assert_called_once_with('list_all', 1, ham='eggs')

    def test_protocol_initialised(self):
        """Test that the factory function for creating a protocol will be called."""
        client.initialise_protocol = Mock(return_value=123)

        gc = client.GearClient('localhost', 1234, protocol=55, ham='eggs')
        assert gc.protocol == 123
        client.initialise_protocol.assert_called_once_with(55, 'localhost', 1234, ham='eggs')
