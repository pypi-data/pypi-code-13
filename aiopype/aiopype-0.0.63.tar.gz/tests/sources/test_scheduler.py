#pylint: disable=E0401
"""
Test scheduler sources.
"""
import asyncio
from unittest import mock
from unittest import TestCase

from aiopype.sources import CronJob
from aiopype.messaging import SyncEventHandler

class TestScheduler(TestCase):
  def test_scheduler(self):
    mock_handler = SyncEventHandler()
    scheduler = CronJob('cron', mock_handler, frequency = 1, interval = 1)

    timestamps = []
    def handler(timestamp):
      timestamps.append(timestamp)
      if len(timestamps) == 3:
        scheduler.done = True

    scheduler.on('cron', handler)
    asyncio.get_event_loop().run_until_complete(scheduler.start())
    self.assertEqual(timestamps[0], timestamps[1] - 1)
    self.assertEqual(timestamps[1], timestamps[2] - 1)
