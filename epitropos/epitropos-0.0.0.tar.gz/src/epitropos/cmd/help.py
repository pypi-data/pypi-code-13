# -*- coding: utf-8 -*-
from malibu.command import command_module
from malibu.command.builtins.help import BuiltinHelpModule

import epitropos


@command_module(
    name='help',
    depends=[]
)
class HelpModule(BuiltinHelpModule):

    def __init__(self, loader):

        super(HelpModule, self).__init__(loader)

        self.project_description = (
            'epitropos - a fabulously simple, pluggable OAuth2 server.'
        )
        self.project_version = epitropos.__release__
