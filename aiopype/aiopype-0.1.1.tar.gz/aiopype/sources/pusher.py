import asyncio
import logging
from datetime import datetime, timedelta

import pusherclient

from aiopype.processor import Processor


class PusherClient(pusherclient.Pusher):
  """
  pusherclient.Pusher wrapper with error handling.

  Wraps calls to event handlers around try catch in order to capture exceptions
  to sentry. This is a workaround due to the threaded nature of PusherClient.
  """
  def __init__(self, *args, **kwargs):
    self.exception = None
    self.logger = logging.getLogger('pusherclient')
    kwargs['log_level'] = self.logger.getEffectiveLevel()

    super(PusherClient, self).__init__(*args, **kwargs)

  def _connection_handler(self, *args, **kwargs):
    try:
      super(PusherClient, self)._connection_handler(*args, **kwargs)
    except Exception as err:
      self.exception = err


class PusherClientSource(Processor):
  """
  Pusher Client source.

  Uses thread based pusherclient module, and monitors if the client is running as expected.
  """
  def __init__(self, name, handler, **kwargs):
    super().__init__(name, handler)
    self.done = False
    self.heartbeat_timeout = kwargs.get('heartbeat_timeout', 30)
    self.last_heartbeat = datetime.now()
    self.logger = logging.getLogger(name)
    self.pusher = PusherClient(kwargs.get('pusher', ''))

  async def start(self):
    """
    Initializes the Pusher client and exception / disconnected / heartbeat_timeout handlers.
    """
    self.pusher.connection.bind('pusher:connection_established', self.connect_handler)
    self.pusher.connect()

    try:
      while True:
        # Check pusher.exception and raise it.
        if self.pusher.exception:
          self.done = True
          raise self.pusher.exception

        # Check pusher.connection state.
        if self.pusher.connection.state in ('failed', 'disconnected'):
          self.done = True
          raise Exception("Connection to pusherclient lost {}".format(self.pusher.connection.state))

        if datetime.now() - self.last_heartbeat > timedelta(seconds = self.heartbeat_timeout):
          self.done = True
          raise Exception('Lost heartbeat for more than threshold value')

        await asyncio.sleep(0.5)
    finally:
      self.done = True

  def connect_handler(self, _):
    """
    The connection_established handler.

    Should subscribe to channels here.
    """
    pass
