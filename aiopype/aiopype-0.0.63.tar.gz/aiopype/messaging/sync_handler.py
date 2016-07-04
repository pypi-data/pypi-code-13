import asyncio
from pyee import EventEmitter

class SyncEventHandler(EventEmitter):
  async def emit_async(self, event, *args, **kwargs):
    """
    Emit asynchrounously.

    This method should be promoted to a Pull Request to pyee.
    """
    handled = False

    # Copy the events dict first. Avoids a bug if the events dict gets
    # changed in the middle of the following for loop.
    events_copy = list(self._events[event])

    # Pass the args to each function in the events dict
    for handler in events_copy:
      if asyncio.iscoroutinefunction(handler):
        await handler(*args, **kwargs)
      else:
        handler(*args, **kwargs)
      handled = True

    if not handled and event.split('__')[-1] == 'error':
      raise Exception('Uncaught error event.')

    return handled

  def get_events(self):
    return self._events.keys()

  def once(self, event, f = None):
    """
    Override to accomodate async handlers
    """
    def _once(handler):
      if asyncio.iscoroutinefunction(handler):
        async def new_handler(*args, **kwargs):
          await handler(*args, **kwargs)
          self.remove_listener(event, new_handler)
      else:
        def new_handler(*args, **kwargs):
          handler(*args, **kwargs)
          self.remove_listener(event, new_handler)
      return new_handler

    def _wrapper(handler):
      self.on(event, _once(handler))
      return handler

    if f is None:
      return _wrapper
    else:
      _wrapper(f)
