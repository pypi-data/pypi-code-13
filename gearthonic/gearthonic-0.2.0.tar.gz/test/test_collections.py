"""Tests for the collections"""

from mock import Mock

from gearthonic.methods import BaseCollection


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
