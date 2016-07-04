"""
Time Sources.
"""
import asyncio
from datetime import datetime

from aiopype.processor import Processor


class TimeSource(Processor):
  def __init__(self, name, handler, interval):
    super().__init__(name, handler)
    self.interval = interval
    self.loop = asyncio.get_event_loop()

  def get_time(self):
    next_time = datetime.now().timestamp()
    next_time -= next_time % self.interval
    return next_time

  async def start(self):
    await self.emit_async('cron', self.get_time())
    self.done = True


class OffsetTimeSource(TimeSource):
  def __init__(self, name, handler, interval, offset):
    super().__init__(name, handler, interval)
    self.offset = offset

  def get_time(self):
    next_time = datetime.now().timestamp() - self.offset
    next_time -= next_time % self.interval
    return next_time
