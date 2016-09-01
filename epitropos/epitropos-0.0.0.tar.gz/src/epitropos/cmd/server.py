# -*- coding: utf-8 -*-
from __future__ import print_function

import epitropos
import traceback

from malibu.command import command_module
from malibu.command.module import CommandModule
from malibu.util.scheduler import Scheduler
from restify import routing
from restify.manager import RESTAPIManager


@command_module(
    name='server',
    depends=['config']
)
class ServerModule(CommandModule):

    def __init__(self, loader):

        super(ServerModule, self).__init__()
        self.__loader = loader

        self.register_subcommand('start', self.server_start)

    def server_start(self, *args, **kw):
        """ server:start [...]

            Starts the server.
        """

        from epitropos import plugin

        cfg = self.__loader.get_module_by_base('config').get_configuration()

        manager = RESTAPIManager(config=cfg)

        scheduler = Scheduler()
        scheduler.save_state('epitropos')

        plugin.load_plugins()
        plugin.load_active_plugins(cfg)
        plugin.storage().connect()

        manager.load_logging()
        manager.load_bottle()
        routing.load_routing_modules(manager, package='epitropos.routes')
        manager.load_dsn()

        manager.dsn.client.release = epitropos.__release__

        try:
            manager.run_bottle()
        except:
            if manager.dsn:
                manager.dsn.client.captureException()
            else:
                traceback.print_exc(5)
