import asyncio
import json
import logging
from datetime import datetime, timedelta

import aiohttp
import websockets

from aiopype.processor import Processor

PACKET_NAMES = {
  '0': 'disconnect',
  '1': 'connect',
  '2': 'heartbeat',
  '3': 'message',
  '4': 'json',
  '5': 'event',
  '6': 'ack',
  '7': 'error',
  '8': 'noop',
}

PACKET_CODES = {v: k for k, v in PACKET_NAMES.items()}


class SocketIOPacketException(Exception):
  pass


class SocketIOPacket(object):
  def __init__(self, packet_type, name, data):
    self.data = data
    self.name = name
    self.packet_type = packet_type
    self.packet_code = PACKET_CODES[self.packet_type]

  @classmethod
  def parse(cls, packet):
    parts = packet.split(':')
    return cls(PACKET_NAMES[parts[0]], None, ':'.join(parts[3:]))

  def __str__(self):
    parts = [
      self.packet_code,
      '',
      ''
    ]
    if self.packet_code == '5':
      parts.append(json.dumps({
        'name': self.name,
        'args': [self.data]
      }))
    return ':'.join(parts)


class SocketIOSource(Processor):
  response_factory = SocketIOPacket
  source = 'localhost'

  def __init__(self, name, handler, *args, **kwargs):
    super().__init__(name, handler)
    self.done = None
    self.failures = 0
    self.last_heartbeat = datetime.now()
    self.logger = logging.getLogger(name)
    self.loop = asyncio.get_event_loop()
    self.max_failures = kwargs.get('exception_threshold', 10)
    self.heartbeat_timeout = kwargs.get('heartbeat_timeout', 60)
    self.on('connected', self.on_connect)
    self.on('disconnect', self.on_disconnect)
    self.on('error', self.on_error)
    self.on('heartbeat', self.handle_heartbeat)
    self.running = True
    self.websocket = None

  async def on_connect(self):
    pass

  async def on_error(self, _):
    self.websocket.close()
    self.logger.warning('Got unexpected error')
    raise websockets.ConnectionClosed(None, None)

  async def on_disconnect(self, _):
    self.logger.warning("Disconnected")
    self.failures += 1
    if self.failures > self.max_failures:
      self.running = False

  async def get_url(self):
    with aiohttp.ClientSession() as session:
      response = await session.post('http://{}/socket.io/1/'.format(self.source))
      data = await response.text()
      hskey = data.split(':')[0]

    return 'ws://{}/socket.io/1/websocket/{}'.format(self.source, hskey)

  async def start(self):
    try:
      while self.running:
        self.last_heartbeat = datetime.now()
        await self.watchdog(self.connect())
    finally:
      self.done = True
      raise Exception("Disconnected too many times, stopped")

  async def connect(self):
    try:
      url = await self.get_url()

      async with websockets.connect(url) as self.websocket:
        self.logger.debug('Connected to websocket {}'.format(url))
        await self.emit_async('connected')

        while self.running:
          data_raw = await self.websocket.recv()
          received = self.response_factory.parse(data_raw)
          await self.emit_async(received.packet_type, received)
          self.failures = 0

    except (websockets.ConnectionClosed, ConnectionResetError, websockets.InvalidHandshake):
      await self.emit_async('disconnect', "Websocket closed")

  async def watchdog(self, coro):
    future = asyncio.ensure_future(coro, loop = self.loop)

    while not future.done() and datetime.now() - self.last_heartbeat < timedelta(seconds = self.heartbeat_timeout):
      await asyncio.sleep(1)

    if not future.done():
      future.cancel()

    await self.emit_async('disconnect', "Lost heartbeat")

  async def handle_heartbeat(self, _):
    self.last_heartbeat = datetime.now()
    request = SocketIOPacket('heartbeat', '', '')
    await self.websocket.send(str(request))
