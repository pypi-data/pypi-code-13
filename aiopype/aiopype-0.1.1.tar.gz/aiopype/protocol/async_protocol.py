import asyncio
from collections import defaultdict

from .sync_protocol import SyncProtocol


class AsyncProtocol(SyncProtocol):
  def __init__(self):
    super().__init__()
    self.running = False
    self.queue = asyncio.Queue()
    self.loop = asyncio.get_event_loop()
    self.on('stop', self.stop)

  def emit(self, event, *args, **kwargs):
    asyncio.ensure_future(self.queue.put((event, args, kwargs)), loop = self.loop)
    return True

  async def emit_async(self, event, *args, **kwargs):
    await self.queue.put((event, args, kwargs))
    return True

  def stop(self):
    self.running = False

  async def listen(self):
    self.running = True
    self.tasks = defaultdict(list)

    try:
      while True:
        event, args, kwargs = await self.queue.get()

        if not self.tasks[event]:
          handled = False
          events_copy = list(self._events[event])

          # Pass the args to each function in the events dict
          for handler in events_copy:
            if asyncio.iscoroutinefunction(handler):
              self.tasks[event].append(asyncio.ensure_future(handler(*args, **kwargs)))
            else:
              handler(*args, **kwargs)
            handled = True

          if not handled and event.split('__')[-1] == 'error':
            raise Exception('Uncaught error event.')
        else:
          self.queue.put((event, args, kwargs))

        for event, tasks in self.tasks.items():
          self.tasks[event] = [task for task in tasks if not task.done()]

    finally:
      self.running = False
      await asyncio.wait_for(asyncio.gather(*self.tasks, return_exceptions = True), 10)
