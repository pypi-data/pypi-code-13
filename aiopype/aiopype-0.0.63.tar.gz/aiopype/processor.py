"""
Processor module.

Responsible for processing incoming data and produce events.
"""

import logging

from aiopype.messaging import EventMixin


class ProcessorRegistry(type):
  """
  Processors metaclass with registry.
  """

  REGISTRY = {}

  def __new__(mcs, name, bases, attrs):
    """ @param name: Name of the class
        @param bases: Base classes (tuple)
        @param attrs: Attributes defined for the class
    """
    new_cls = type.__new__(mcs, name, bases, attrs)
    mcs.REGISTRY[new_cls.__module__ + '.' + new_cls.__name__] = new_cls

    return new_cls

class Processor(EventMixin, metaclass = ProcessorRegistry):
  """
  Processor object.
  """
  def __init__(self, name, handler):
    """
    Constructor.
      @param name: the unique identifier for this processor inside a manager
      @param handler: the central event handler
    """
    self.done = False
    self.name = name
    self.handler = handler
    self.logger = logging.getLogger(name)

  def start(self, loop):
    """
    Method to kickstart sources.

    Must be overriden by source processors.
    """
    raise NotImplementedError()

  def is_done(self):
    """
    Determines if a processor has for some reason stopped.
    """
    return self.done
