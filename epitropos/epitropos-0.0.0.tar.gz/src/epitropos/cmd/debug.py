# -*- coding: utf-8 -*-
from malibu.command import command_module
from malibu.command.module import CommandModule


@command_module(
    name='debug',
    depends=['config']
)
class DebugModule(CommandModule):

    def __init__(self, loader):

        super(DebugModule, self).__init__()
        self.__loader = loader

        self.register_subcommand('repl', self.spawn_repl, aliases=['shell'])

    def spawn_repl(self, *args, **kw):
        """ debug:repl []
            debug:shell []
            Spawns a REPL to manually prod parts of the program.
        """

        # Set up some scope.
        loader = self.__loader  # noqa
        config = loader.get_module_by_base('config').get_configuration()  # noqa

        import pdb  # noqa
        pdb.set_trace()  # noqa
