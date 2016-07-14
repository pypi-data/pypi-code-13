"""
Messaging mixin for processors.
"""
class EventMixin(object):
  """
  Messaging Mixin.
  """
  def on(self, event, func):
    """
    Add handler for event.
    """
    self.handler.on(self.name + '__' + event, func)

  def once(self, event, func):
    """
    Add handler for one time only event.
    """
    self.handler.once(self.name + '__' + event, func)

  def emit(self, event, *args, **kwargs):
    """
    Trigger an event.
    """
    return self.handler.emit(self.name + '__' + event, *args, **kwargs)

  async def emit_async(self, event, *args, **kwargs):
    """
    Trigger an event asynchrounously.

    Returns a coroutine.
    """
    return await self.handler.emit_async(self.name + '__' + event, *args, **kwargs)

  def remove_all_listeners(self, event = None):
    """
    Remove all listeners attached to self.
    """
    if event:
      events = [self.name + '__' + event]
    else:
      events = [event for event in self.handler.get_events() if event.startswith(self.name + '__')]

    for event in events:
      self.handler.remove_all_listeners(event)

  def listeners(self, event):
    """
    Returns the list of all listeners registered to the event.
    """
    return self.handler.listeners(self.name + '__' + event)
