#pylint: disable=E0401
"""
Test SocketIO abstract source.
"""
import asyncio
import json
from unittest import mock
from unittest import TestCase

import websockets

from aiopype.sources import socketio
from aiopype.messaging import SyncEventHandler

class TestSocketIOPacket(TestCase):
  """
  Test huobi packet wrapper.
  """
  def test_packet_str(self):
    packet = socketio.SocketIOPacket('event', 'test', {'some': 'data'})

    packet_str = str(packet)
    packet_message = json.loads(packet_str.split('5:::')[1])

    self.assertTrue(packet_str.startswith('5:::'))
    self.assertEqual(packet_message, {"name": "test", "args": [{"some": "data"}]})

class TestSocketIOSource(TestCase):
  async def sleeper(self, time):
    await asyncio.sleep(time)

  def test_on_error(self):
    mock_handler = SyncEventHandler()
    source = socketio.SocketIOSource('test', mock_handler)
    source.websocket = mock.MagicMock()

    loop = asyncio.get_event_loop()
    exception = None
    try:
      loop.run_until_complete(source.on_error('abc'))
    except Exception as error:
      exception = error

    self.assertTrue(source.websocket.close.called)
    self.assertEqual(type(exception), websockets.ConnectionClosed)

  def test_on_disconnect(self):
    mock_handler = SyncEventHandler()
    source = socketio.SocketIOSource('test', mock_handler)
    source.max_failures = 0
    loop = asyncio.get_event_loop()
    loop.run_until_complete(source.on_disconnect('test'))
    self.assertFalse(source.running)

  @mock.patch('aiopype.sources.socketio.aiohttp')
  def test_get_url(self, aiohttp_mock):
    mock_handler = SyncEventHandler()
    source = socketio.SocketIOSource('test', mock_handler)

    json_future = asyncio.Future()
    json_future.set_result("123123:1231231")
    http_response = mock.Mock()
    http_response.text = mock.Mock(return_value = json_future)

    response_future = asyncio.Future()
    response_future.set_result(http_response)
    http_client = mock.Mock()
    http_client.post = mock.Mock(return_value = response_future)

    session = mock.MagicMock()
    session.__enter__ = mock.Mock(return_value = http_client)
    aiohttp_mock.ClientSession = mock.Mock(return_value = session)

    loop = asyncio.get_event_loop()
    url = loop.run_until_complete(source.get_url())

    self.assertEqual(url, 'ws://localhost/socket.io/1/websocket/123123')

  def test_start(self):
    mock_handler = SyncEventHandler()
    source = socketio.SocketIOSource('test', mock_handler)
    source.connect = mock.Mock(return_value = 'test')
    watch_future = asyncio.Future()
    watch_future.set_result(None)
    source.watchdog = mock.Mock(return_value = watch_future)
    socketio.SocketIOSource.running = mock.PropertyMock(side_effect = [True, True, False])
    exception = None

    try:
      loop = asyncio.get_event_loop()
      loop.run_until_complete(source.start())
    except Exception as error:
      exception = error

    self.assertEqual(str(exception), 'Disconnected too many times, stopped')
    self.assertTrue(source.done)
    source.watchdog.assert_called_with('test')
    socketio.SocketIOSource.running = True

  def test_watchdog(self):
    mock_handler = SyncEventHandler()
    source = socketio.SocketIOSource('test', mock_handler)
    done_future = asyncio.Future()
    done_future.set_result(None)
    source.emit_async = mock.Mock(return_value = done_future)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(source.watchdog(self.sleeper(1)))

    source.emit_async.assert_called_with('disconnect', 'Lost heartbeat')

    source.heartbeat_timeout = 2
    loop = asyncio.get_event_loop()
    coro = self.sleeper(10)
    loop.run_until_complete(source.watchdog(coro))

    source.emit_async.assert_called_with('disconnect', 'Lost heartbeat')

  def test_handle_heartbeat(self):
    mock_handler = SyncEventHandler()
    source = socketio.SocketIOSource('test', mock_handler)
    source.websocket = mock.Mock()
    done_future = asyncio.Future()
    done_future.set_result(None)
    source.websocket.send = mock.Mock(return_value = done_future)
    source.last_heartbeat = None

    loop = asyncio.get_event_loop()
    loop.run_until_complete(source.handle_heartbeat('test'))

    source.websocket.send.assert_called_with('2::')
    self.assertTrue(source.last_heartbeat)
