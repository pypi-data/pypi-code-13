#pylint: disable=E0401
"""
Test websocket source.
"""
import asyncio
from unittest import mock
from unittest import TestCase

from aiopype import SyncProtocol
from aiopype.sources import WebsocketSource


class TestWebsocketSource(TestCase):
  @mock.patch('aiopype.sources.WebsocketSource.on_connect')
  @mock.patch('aiopype.sources.WebsocketSource.on_lost_connection')
  def test_init(self, lost_connection_mock, connected_mock):
    source = WebsocketSource('test', SyncProtocol())
    done_future = asyncio.Future()
    done_future.set_result(None)
    connected_mock.return_value = done_future
    lost_connection_mock.return_value = done_future

    async def test_events():
      await source.emit_async('connected')
      await source.emit_async('disconnected')

    loop = asyncio.get_event_loop()
    loop.run_until_complete(test_events())

    connected_mock.assert_called_with()
    lost_connection_mock.assert_called_with()
    self.assertEqual(source.done, None)
    self.assertEqual(source.failures, 0)
    self.assertEqual(source.max_failures, 10)
    self.assertEqual(source.heartbeat_timeout, 30)

  def test_lost_connection(self):
    source = WebsocketSource('test', SyncProtocol())
    source.max_failures = 0
    loop = asyncio.get_event_loop()
    loop.run_until_complete(source.on_lost_connection())
    self.assertFalse(source.running)

  def test_start(self):
    source = WebsocketSource('test', SyncProtocol())
    source.connect = mock.Mock(return_value = 'test')
    watch_future = asyncio.Future()
    watch_future.set_result(None)
    source.watchdog = mock.Mock(return_value = watch_future)
    WebsocketSource.running = mock.PropertyMock(side_effect = [True, True, False])

    loop = asyncio.get_event_loop()
    exception = None

    try:
      loop.run_until_complete(source.start())
    except Exception as error:
      exception = error
    self.assertEqual(str(exception), 'Disconnected too many times, stopped')
    self.assertTrue(source.done)
    source.watchdog.assert_called_with('test')
    WebsocketSource.running = True

  def test_parse(self):
    parsed = WebsocketSource.parse("[1, 2, 3]")
    self.assertEqual(parsed, [1, 2, 3])


class TestWebsocketSourceWatchdog(TestCase):
  def setUp(self):
    self.source = WebsocketSource('test', SyncProtocol())
    self.loop = asyncio.get_event_loop()

    done_future = asyncio.Future()
    done_future.set_result(None)
    self.source.emit_async = mock.Mock(return_value = done_future)

  async def sleeper(self, time):
    await asyncio.sleep(time)

  def test_finish_before_websocket(self):
    self.loop.run_until_complete(self.source.watchdog(self.sleeper(1)))
    self.source.emit_async.assert_called_with('disconnected', 'Service failed')

  def test_timeout_before_websocket(self):
    self.source.heartbeat_timeout = 0.01
    self.loop.run_until_complete(self.source.watchdog(self.sleeper(1)))
    self.source.emit_async.assert_called_with('disconnected', 'Unable to connect')

  def test_coroutine_done(self):
    self.source.websocket = mock.Mock()
    pong_future = asyncio.Future()
    pong_future.set_result(asyncio.ensure_future(self.sleeper(1)))
    self.source.websocket.ping = mock.Mock(return_value = pong_future)

    self.loop.run_until_complete(self.source.watchdog(self.sleeper(1)))
    self.source.emit_async.assert_called_with('disconnected', 'Service failed')

  def test_lost_heartbeat(self):
    self.source.websocket = mock.Mock()
    self.source.heartbeat_timeout = 0.01
    pong_future = asyncio.Future()
    pong_future.set_result(asyncio.ensure_future(self.sleeper(10)))
    self.source.websocket.ping = mock.Mock(return_value = pong_future)

    self.loop.run_until_complete(self.source.watchdog(self.sleeper(1)))
    self.source.emit_async.assert_called_with('disconnected', 'Lost heartbeat')
