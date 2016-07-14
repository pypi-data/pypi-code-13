"""
Time Sources.
"""
import asyncio
from datetime import datetime

from aiopype.processor import Processor


def get_rounded_timestamp(interval):
  time = datetime.now().timestamp()
  time -= time % interval
  return time


class TimeSource(Processor):
  def __init__(self, name, handler, interval):
    super().__init__(name, handler)
    self.interval = interval
    self.loop = asyncio.get_event_loop()

  def get_time(self):
    return get_rounded_timestamp(self.interval)

  async def start(self):
    await self.emit_async('cron', self.get_time())
    self.done = True


class OffsetTimeSource(TimeSource):
  def __init__(self, name, handler, interval, offset):
    super().__init__(name, handler, interval)
    self.offset = offset

  def get_time(self):
    return get_rounded_timestamp(self.interval) - self.offset
