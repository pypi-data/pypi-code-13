from dj_impediments import get_impediments
from django.test import SimpleTestCase
try:
    from unittest import mock
except ImportError:
    from mock import mock


class GetImpedimentsTestCase(SimpleTestCase):
    @mock.patch('dj_impediments.cache._get_impediments')
    def test_first_call(self, mock_get_impediments):
        mock_get_impediments.return_value = [{'type': 'U'}]

        impediments = get_impediments()

        self.assertEqual(impediments, [{'type': 'U'}])
        mock_get_impediments.assert_any_call()

    @mock.patch('dj_impediments.cache._get_impediments')
    def test_second_call(self, mock_get_impediments):
        mock_get_impediments.return_value = [{'type': 'U'}]

        impediments = get_impediments()

        self.assertEqual(impediments, [{'type': 'U'}])
        mock_get_impediments.assert_not_called()
