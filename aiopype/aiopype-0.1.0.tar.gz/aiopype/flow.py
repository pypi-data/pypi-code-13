"""
Main module

Contains the persister singleton.
"""
import asyncio
import logging
import sys

from raven import Client

from .manager import ManagerRegistry
from .protocol import AsyncProtocol, SyncProtocol


class Flow(object):
  """
  Persister entrypoint

  Responsible for orchestration, error handling and report.
  """
  def __init__(self, config):
    self.config = config
    self.logger = logging.getLogger('persister')
    if not hasattr(config, 'RAVEN_DSN'):
      config.RAVEN_DSN = None
    if config.RAVEN_DSN:
      self.raven = Client(config.RAVEN_DSN, release = config.VERSION)
    else:
      self.raven = None

    self.loop = asyncio.get_event_loop()
    self.loop.set_exception_handler(self.handle_exception)

  def handle_exception(self, _, data):
    if 'exception' in data:
      exception = data['exception']
      self.logger.warning(exception)

      exception_info = (type(exception), exception, exception.__traceback__)

      if self.raven:
        self.raven.captureException(exception_info)
      else:
        self.logger.info('Unable to capture exception on raven', extra = {'info': exception_info})

      self.logger.debug("Reported to sentry, will restart manager")
      asyncio.ensure_future(self.check_managers(), loop = self.loop)

  async def check_managers(self):
    self.logger.debug("Checking for stopped managers")

    done_managers = [manager for manager in self.managers if manager.done()]

    self.logger.debug('Stopped: ' + str(done_managers))

    for manager in done_managers:

      if manager.should_restart():
        manager.remove_all_listeners()
        factory = ManagerRegistry.REGISTRY[manager.name]
        new_manager = factory(self.handler)
        new_manager.start(self.loop)
        self.managers.append(new_manager)

      self.managers.remove(manager)

  async def finished(self):
    while self.managers:
      await asyncio.sleep(4)
      self.managers = [manager for manager in self.managers if manager.should_restart() or not manager.done()]
    self.logger.debug("All managers are done")

  def start(self):
    self.managers = []
    self.handler = SyncProtocol()
    flows = self.config.FLOWS

    for manager_factory in [ManagerRegistry.REGISTRY[x] for x in flows]:
      manager = manager_factory(self.handler)
      manager.start(self.loop)
      self.managers.append(manager)

    self.loop.run_until_complete(self.finished())


class AsyncFlow(Flow):
  async def check_managers(self):
    self.logger.debug("Checking for stopped managers")

    done_managers = [manager for manager in self.managers if manager.done()]

    self.logger.debug('Stopped: ' + str(done_managers))

    for manager in done_managers:

      if manager.should_restart():
        manager.remove_all_listeners()
        factory = ManagerRegistry.REGISTRY[manager.name]
        new_manager = factory(self.handler)
        new_manager.start(self.loop)
        self.managers.append(new_manager)

      self.managers.remove(manager)

    if not self.handler.running:
      self.logger.error("Listener stopped, restarting.")
      self.handler_task = asyncio.ensure_future(self.check_listener())

  async def check_listener(self):
    await self.handler.listen()

  async def finished(self):
    await super().finished()
    await self.handler.emit_async('stop')
    await self.handler_task
    self.logger.debug("Messaging handler done")

  def start(self):
    self.managers = []
    self.handler = AsyncProtocol()
    flows = self.config.FLOWS

    for manager_factory in [ManagerRegistry.REGISTRY[x] for x in flows]:
      manager = manager_factory(self.handler)
      manager.start(self.loop)
      self.managers.append(manager)

    self.handler_task = asyncio.ensure_future(self.check_listener(), loop = self.loop)
    self.loop.run_until_complete(self.finished())
