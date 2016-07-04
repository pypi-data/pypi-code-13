#pylint: disable=E0401
"""
Test processor.
"""
import asyncio
from unittest import TestCase

from aiopype.processor import Processor
from aiopype.messaging import SyncEventHandler

class TestProcessor(TestCase):
  def test_emit_async(self):
    """
    Test processor's emit_async.
    """
    self.async_called = False
    self.sync_called = True

    async def async_handler():
      """
      Async handler.
      """
      await asyncio.sleep(1)
      self.async_called = True

    def sync_handler():
      """
      Sync handler.
      """
      self.sync_called = True

    async def run_emit():
      handled = await event_emitter.emit_async('test')
      self.assertTrue(handled)

    event_emitter = Processor('test', SyncEventHandler())

    event_emitter.once('test', async_handler)
    event_emitter.once('test', sync_handler)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_emit())

    self.assertTrue(self.async_called)
    self.assertTrue(self.sync_called)

  def test_is_done(self):
    processor = Processor('test', SyncEventHandler())
    self.assertFalse(processor.is_done())

    processor.done = True
    self.assertTrue(processor.is_done())

  def test_exception_without_handler(self):
    """
    Test exception without handler.
    """
    event_emitter = Processor('test', SyncEventHandler())
    exception = None

    async def run_emit():
      await event_emitter.emit_async('error')

    try:
      loop = asyncio.get_event_loop()

      loop.run_until_complete(run_emit())
    except Exception as err:
      exception = err

    self.assertEqual(str(exception), 'Uncaught error event.')
