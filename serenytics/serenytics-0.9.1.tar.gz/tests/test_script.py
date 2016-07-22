import pytest


class TestScript(object):

    @pytest.fixture(autouse=True)
    def set_test_client(self, serenytics_client, script_test):
        self._client = serenytics_client
        self._script = script_test

    def test_run_synchronously(self):
        result = self._script.run(async=False)
        assert result == {
            'stdout': 'Hello, Serenytics!\n',
            'return_code': 0,
            'stderr': '',
            'execution_status': 'SUCCESS'
        }
