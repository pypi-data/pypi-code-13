"""
Cron Scheduler.
"""
import asyncio
from datetime import datetime

from aiopype.processor import Processor


class CronJob(Processor):
  def __init__(self, name, handler, frequency, interval):
    super().__init__(name, handler)
    self.done = False
    self.frequency = frequency
    self.interval = interval
    self.loop = asyncio.get_event_loop()

  def transform_time(self, next_time):
    return next_time - self.interval - (next_time % self.interval)

  async def start(self):
    try:
      while not self.done:
        next_time = datetime.now().timestamp() + self.frequency
        next_time -= next_time % self.frequency
        await asyncio.sleep(next_time - datetime.now().timestamp())
        await self.emit_async('cron', self.transform_time(next_time))
    finally:
      self.done = True


class OffsetCronJob(CronJob):
  def __init__(self, name, handler,frequency, interval, offset):
    super().__init__(name, handler, frequency, interval)
    self.offset = offset

  def transform_time(self, next_time):
    return next_time - self.interval - (next_time % self.interval) - self.offset


class HistoryTimeEmitter(Processor):
  def __init__(self, name, handler, start, interval, end):
    super().__init__()
    self.done = False
    self.end_time = end
    self.handler = handler
    self.interval = interval
    self.name = name
    self.start_time = start

  async def start(self):
    try:
      current = self.start_time
      while current < self.end_time:
        await self.emit_async('cron', current)
        current += self.interval
    finally:
      self.done = True
