# -*- coding: utf-8 -*-

import logging

from bsnode import tools
from bsnode import logtool
from bsnode.manage.rm import rm_node
from bsnode.manage.pwd import PwdManager
from bsnode.check import check_options
from bsnode.make.steam.define import Steam
from bsnode.make.steam import steam_games_list

logger = logging.getLogger(__name__)


def entry(**kwargs):
    logtool.logging_init(kwargs.pop('verbose_console', False))

    if not check_options(**kwargs):
        # todo: send alert
        logger.critical('checking options {} is failure'.format(kwargs))
        return False

    if 'make' in kwargs:
        gs = GameServer(**kwargs.pop('make'))
        result = gs.make()

    elif 'restart' in kwargs:
        pwd = PwdManager(kwargs['restart']['node_name'])
        result = pwd.restart()

    elif 'stop' in kwargs:
        pwd = PwdManager(kwargs['stop']['node_name'])
        result = pwd.stop()

    elif 'start' in kwargs:
        pwd = PwdManager(kwargs['start']['node_name'])
        result = pwd.start()

    elif 'remove' in kwargs:
        result = rm_node(kwargs['remove']['node_name'])

    else:
        result = False

    # todo: send notification
    if result:
        logger.info('success')
        return True
    else:
        logger.critical('failed')
        return False


class GameServer:
    def __init__(self, **kwargs):
        self.options = kwargs

    def make(self):
        game = self.options.get('game')

        if not tools.user_add(self.options.get('node_name')):
            return False

        if game in steam_games_list:
            logger.info('detected Steam game')
            steam = Steam(**self.options)
            return steam.define()
        else:
            logger.critical('UNKNOWN game')
            return False
