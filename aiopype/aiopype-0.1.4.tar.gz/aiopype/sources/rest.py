"""
Collector for REST api endpoints.
"""
import asyncio
import logging
from datetime import datetime

import aiohttp
from aiopype import Processor


class RestSource(Processor):
  """
  Data source that relies on http polling to gather new data.
  """
  running = True

  def __init__(self, name, handler, url, options):
    super().__init__(name, handler)
    self.done = False
    self.logger = logging.getLogger(name)
    self.loop = asyncio.get_event_loop()
    self.options = options
    self.tasks = []
    self.tryouts = 0
    self.url = url

  async def start(self):
    """
    Main loop function.

    This loop runs until running is set to False, or an exception arises. While
    it is running, it constantly triggers http requests with an interval of
    `request_interval` seconds.
    Exceptions are not handled here so that the default handler can define
    the behavior on such events.
    """
    try:
      while self.running:
        task = asyncio.ensure_future(self.get_data(), loop = self.loop)
        self.tasks.append(task)
        await asyncio.sleep(self.options['request_interval'])
        done = [task for task in self.tasks if task.done()]
        self.tasks = [task for task in self.tasks if not task.done()]

        for task in done:
          await task

    finally:
      self.logger.debug("I have to wait for my tasks", extra = {'tasks': str(self.tasks)})

      try:
        await asyncio.wait_for(asyncio.gather(*self.tasks, return_exceptions = True), 10)
      finally:
        self.done = True

  def error_handler(self, error):
    self.logger.warning(error)

  async def get_data(self):
    """
    The method that is triggered every `request_interval` seconds and is Responsible
    for performing the HTTP request and emiting the obtained data.
    """
    try:
      with aiohttp.Timeout(8):
        response = await aiohttp.request('get', self.url)
        cur_time = datetime.strptime(response.headers['date'], '%a, %d %b %Y %H:%M:%S %Z').timestamp()
        data = await response.json()

      self.emit('data', data, int(cur_time))
      self.tryouts = 0

    except asyncio.TimeoutError:
      return

    except Exception as err:
      self.tryouts += 1

      if self.tryouts > self.options['exception_threshold']:
        self.error_handler(err)
