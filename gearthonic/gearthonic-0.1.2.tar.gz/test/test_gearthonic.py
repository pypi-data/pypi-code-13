"""
Tests for `gearthonic` module.
"""
import pytest
from mock import Mock
from gearthonic import GearClient
from gearthonic.methods import BaseCollection


@pytest.fixture
def gear_client():
    return GearClient('host', 1234)


class TestGearClient(object):
    """Tests the base GearClient"""

    def test_magic_call(self, gear_client, monkeypatch):
        """Tests that any call gets redirected to the ``call`` method of the GearClient"""
        call_mock = Mock()
        monkeypatch.setattr(gear_client, 'call', call_mock)
        gear_client.list_all(1, ham='eggs')

        assert call_mock.called
        call_mock.assert_called_once_with('list_all', 1, ham='eggs')

    def test_call_method(self, gear_client, monkeypatch):
        """Tests that the call method redirects any call to the XML RPC ServerProxy"""
        call_mock = Mock()
        monkeypatch.setattr(gear_client, 'proxy', call_mock)
        gear_client.call('list_all', 1, ham='eggs')

        assert call_mock.list_all.called
        call_mock.list_all.assert_called_once_with(1, ham='eggs')


class TestBaseCollection(object):
    """Tests the BaseCollection"""

    def test_collection_uses_call_method(self, gear_client, monkeypatch):
        """Tests that the BaseCollection uses the call method of the GearClient"""
        call_mock = Mock()
        # Mock the call method of the GearClient to check, if it got called
        monkeypatch.setattr(gear_client, 'call', call_mock)
        bc = BaseCollection(gear_client)
        bc.call('list_all', 1, ham='eggs')

        assert call_mock.called
        call_mock.assert_called_once_with('list_all', 1, ham='eggs')
