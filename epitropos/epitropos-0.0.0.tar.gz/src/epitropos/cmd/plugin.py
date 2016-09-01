# -*- coding: utf-8 -*-
from __future__ import print_function

from epitropos import plugin
from malibu.command import command_module
from malibu.command.module import CommandModule
from malibu.text.table import TextTable


@command_module(
    name='plugin',
    depends=[]
)
class PluginModule(CommandModule):

    def __init__(self, loader):

        super(PluginModule, self).__init__()
        self.__loader = loader

        self.register_subcommand('list', self.plugin_list)
        self.register_subcommand('requirements', self.plugin_requirements)

    def plugin_list(self, *args, **kw):
        """ plugin:list []

            Lists all of the plugins available to epitropos in table form.
        """

        plugin.load_plugins(pkg_reload=False)

        tt = TextTable(min_width=18)
        tt.add_header_list(['Name', 'Type', 'Class'])

        for pltype in plugin.__plugins__.keys():
            plugin_env = plugin.__plugins__[pltype]
            if isinstance(plugin_env, dict):
                for plug, attrs in plugin_env.items():
                    tt.add_data_ztup(
                        [(attrs.get('name', 'unknown'),
                          pltype,
                          plug,)])
                    continue
            elif isinstance(plugin_env, list):
                for plug in plugin_env:
                    tt.add_data_ztup(
                        [(plug.__class__.__name__,
                          pltype,
                          plug,)])

        for line in tt.format():
            print(line)

    def plugin_requirements(self, *args, **kw):
        """ plugin:requirements []

            Prints all requirements needed for all plugins.
        """

        plugin.load_plugins(pkg_reload=False)

        for pcls, attr in plugin.get_plugins().items():
            name = attr.get('name', str(pcls))
            print("""# requirements for plugin %s""" % (name))
            for req in pcls.requirements():
                print(req)
