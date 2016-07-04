import asyncio
import json
import logging

import websockets

from aiopype.processor import Processor


class WebsocketSource(Processor):
  url = None

  def __init__(self, name, handler, *args, **kwargs):
    super().__init__(name, handler)
    self.done = None
    self.loop = asyncio.get_event_loop()
    self.logger = logging.getLogger(name)
    self.running = True
    self.websocket = None
    self.failures = 0
    self.max_failures = kwargs.get('exception_threshold', 10)
    self.heartbeat_timeout = kwargs.get('heartbeat_timeout', 30)
    self.on('connected', self.on_connect)
    self.on('disconnected', self.on_lost_connection)

  async def on_connect(self):
    pass

  async def on_lost_connection(self, reason = 'Websocket Closed'):
    self.logger.warning('Disconnected', extra = {'reason': reason})
    self.failures += 1
    if self.failures > self.max_failures:
      self.running = False

  async def start(self):
    try:
      while self.running:
        await self.watchdog(self.connect())
    finally:
      self.done = True
      raise Exception('Disconnected too many times, stopped')

  async def connect(self):
    try:
      self.logger.debug('Connecting')
      async with websockets.connect(self.url) as self.websocket:
        self.logger.debug('Connected to websocket {}'.format(self.url))
        await self.emit_async('connected')

        while self.running:
          data_raw = await self.websocket.recv()
          received = self.parse(data_raw)
          await self.emit_async('message', received)
          self.failures = 0

    except (websockets.ConnectionClosed, ConnectionResetError, websockets.InvalidHandshake):
      await self.emit_async('disconnected')

  async def watchdog(self, coro):
    main_loop = asyncio.ensure_future(coro, loop = self.loop)
    websocket_timeout = 0

    while not self.websocket:
      if main_loop.done():
        await self.emit_async('disconnected', 'Service failed')
        return

      await asyncio.sleep(1)
      websocket_timeout += 1

      if websocket_timeout > self.heartbeat_timeout:
        main_loop.cancel()
        await self.emit_async('disconnected', 'Unable to connect')
        return

    while not main_loop.done():
      pong = await self.websocket.ping()
      done, pending = await asyncio.wait([main_loop, pong], timeout = self.heartbeat_timeout)

      if pong not in done:
        main_loop.cancel()
        await self.emit_async('disconnected', 'Lost heartbeat')
        return

      if main_loop in done:
        self.logger.debug(str(main_loop))
        await self.emit_async('disconnected', 'Service failed')
        return

  @staticmethod
  def parse(message):
    return json.loads(message)
