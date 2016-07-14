#pylint: disable=E0401, R0201
import asyncio
from unittest import mock
from unittest import TestCase

from aiopype.sources import RestSource


class TestRestSource(TestCase):
  def setUp(self):
    options = {
      'request_interval': 0.1
    }
    self.mock_handler = mock.MagicMock()
    self.source = RestSource('test', self.mock_handler,'test', options)
    self.loop = asyncio.get_event_loop()

  @mock.patch('aiopype.sources.rest.RestSource.running', new_callable = mock.PropertyMock)
  @mock.patch('aiopype.sources.rest.RestSource.get_data')
  def test_get_data_invoked(self, get_data_mock, running_mock):

    running_mock.side_effect = [True, True, False]
    future = asyncio.Future(loop = self.loop)
    future.set_result(None)
    get_data_mock.return_value = future

    async def test():
      await self.source.start()
      self.assertTrue(get_data_mock.called)

    self.loop.run_until_complete(test())

  @mock.patch('aiopype.sources.rest.RestSource.emit')
  @mock.patch('aiopype.sources.rest.aiohttp.request')
  def test_data_emit(self, request_mock, emit_mock):

    async def test():
      future_json = asyncio.Future(loop = self.loop)
      future_json.set_result({'some': 'data'})
      response = mock.Mock()
      response.headers = {'date': 'Thu, 25 Feb 2016 17:46:46 UTC'}
      response.json = mock.Mock(return_value = future_json)

      response_future = asyncio.Future(loop = self.loop)
      response_future.set_result(response)
      request_mock.return_value = response_future

      await self.source.get_data()

    self.loop.run_until_complete(test())
    emit_mock.assert_called_with('data', {'some': 'data'}, 1456422406)
