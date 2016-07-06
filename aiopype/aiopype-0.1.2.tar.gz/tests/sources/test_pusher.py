#pylint: disable=E0401
"""
Test Pusher client source.
"""
import asyncio
from unittest import mock
from unittest import TestCase

from aiopype.sources import PusherClientSource


class TestPusherClientSource(TestCase):
  def test_start(self):
    mock_handler = mock.MagicMock()
    source = PusherClientSource('test', mock_handler)
    source.pusher = mock.MagicMock()
    type(source.pusher).exception = mock.PropertyMock(side_effect = [None, 'a', Exception('forcequit')])

    loop = asyncio.get_event_loop()

    try:
      loop.run_until_complete(source.start())
    except Exception as error:
      self.assertEqual(str(error), 'forcequit')

    self.assertTrue(source.done)

    type(source.pusher).exception = mock.PropertyMock(return_value = None)
    type(source.pusher.connection).state = mock.PropertyMock(return_value = 'failed')

    try:
      loop.run_until_complete(source.start())
    except Exception as error:
      self.assertEqual(str(error), 'Connection to pusherclient lost failed')
