import asyncio
import logging

from aiopype.messaging import SyncEventHandler
from .processor import ProcessorRegistry

class ManagerRegistry(type):
  REGISTRY = {}

  def __new__(mcs, name, bases, attrs):
    """ @param name: Name of the class
        @param bases: Base classes (tuple)
        @param attrs: Attributes defined for the class
    """
    new_cls = type.__new__(mcs, name, bases, attrs)
    mcs.REGISTRY[new_cls.name] = new_cls

    return new_cls


class Manager(metaclass = ManagerRegistry):
  name = "default_manager"
  source = None
  run_always = True

  def __init__(self, handler = SyncEventHandler()):
    self.handler = handler
    self.logger = logging.getLogger(self.name)

  def build_processor_name(self, name):
    return '.'.join([self.name, name])

  def get_source(self):
    return self.source

  def done(self):
    if self.source:
      return self.source.is_done()

  def should_restart(self):
    return self.run_always

  def start(self, loop):
    asyncio.ensure_future(self.get_source().start(), loop = loop)

  def remove_all_listeners(self):
    """
    Remove all listeners attached to self.
    """
    events = [event for event in self.handler.get_events() if event.startswith(self.name + '.')]

    for event in events:
      self.handler.remove_all_listeners(event)

class DescriptiveManager(Manager, metaclass = ManagerRegistry):
  processors = {}
  flows = []

  def __init__(self, handler = SyncEventHandler()):
    super().__init__(handler)
    for name, metadata in self.processors.items():
      processor = ProcessorRegistry.REGISTRY[metadata['cls']](self.build_processor_name(name), self.handler, *metadata['args'], **metadata['kwargs'])
      setattr(self, name, processor)

    for flow in self.flows:
      origin = getattr(self, flow['origin'])
      target = getattr(self, flow['target'])
      target_function = getattr(target, flow['function'])
      origin.on(flow['event'], target_function)
