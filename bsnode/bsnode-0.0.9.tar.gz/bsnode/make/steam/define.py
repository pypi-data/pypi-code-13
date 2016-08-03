# -*- coding: utf-8 -*-

import os
import shutil
import logging

import bsnode
import bsnode.ports
import bsnode.tools as tools

import pyscfg
import bsstatusflags.flag


logger = logging.getLogger(__name__)


class Steam:
    alias_cache_dirs = {
        'dod': 'day_of_defeat_source',
        'css': 'counter_strike_source',
        'cs_go': 'counter_strike_global_offensive'}
    tpls_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'templates')
    default_range_ports = range(27200, 20399)

    def __init__(self, **kwargs):
        logger.info('init steam module with options: {}'.format(kwargs))
        self.conf = pyscfg.Config(bsnode.general_conf, 'bsnode')
        self.node_name = kwargs.get('node_name')
        self.game = kwargs.get('game')
        self.slots = kwargs.get('slots')
        self.port = None

        if self.conf.range_ports:
            min_, max_ = self.conf.range_ports.split(',')
            self.range_ports = range(int(min_), int(max_))
        else:
            logger.warning('range ports not defined, using default {}'.format(
                self.default_range_ports))
            self.range_ports = self.default_range_ports

    def define(self):
        logger.info('define node {}'.format(self.node_name))

        port = bsnode.ports.Ports(self.node_name, self.range_ports)
        self.port = port.get()

        if self.port:
            logger.info('game port is {}'.format(self.port))
        else:
            logger.critical('game port not defined')

        if not self.copy_cache():
            return False

        if not self.template_render():
            return False

        logger.info('attempt start node {}'.format(self.node_name))
        if not tools.start_node(self.node_name):
            return False

        logger.info('success defined the node {}, game {}, port {}'.format(
            self.node_name, self.game, self.port))
        return True

    def copy_cache(self):
        logger.info('begin coping the cache {}'.format(self.game))
        status = bsstatusflags.flag.Flag()
        node_dir = os.path.join(self.conf.nodes_dir, self.node_name, self.game)

        logger.info('attempt setting a flag that cache {} is busy'.format(
            self.game))

        if not status.action('{}_cache'.format(self.game), set_=True):
            logger.critical('failed setting flag')
            return False

        try:
            try:
                logger.info('start copping the cache')
                shutil.copytree(
                    src=os.path.join(
                        self.conf.cache_dir, self.alias_cache_dirs[self.game]),
                    dst=node_dir)
            except FileExistsError:
                logger.critical('cache already exists (?!?!?)')
                return False
        finally:
            logger.info('delete the flag after success operation')
            status.action('{}_cache'.format(self.game), del_=True)

        sdk32_dir = os.path.join(
            self.conf.nodes_dir, self.node_name, '.steam/sdk32')
        os.makedirs(sdk32_dir, exist_ok=True)

        logger.info('create link to steamclient.so')

        if not tools.ln(
                os.path.join(node_dir, 'bin/steamclient.so'),
                os.path.join(sdk32_dir, 'steamclient.so')):
            return False

        logger.info('change permission to server folder')

        if not tools.change_own(self.node_name, self.node_name, node_dir):
            return False

        logger.info('success coping cache')
        return True

    def template_render(self):
        logger.info('begin render template for game {}'.format(self.game))

        default_opts = {
            'dod': {'mod': 'dod', 'map': 'dod_flash'},
            'css': {'mod': 'cstrike', 'map': 'de_dust2'},
            'cs_go': {'mod': 'csgo', 'map': 'de_dust2'}}

        dst = os.path.join(
            self.conf.supervisor_conf_dir, self.node_name + '.conf')

        logger.info('destination file {}'.format(dst))

        tpl_data = {
            'node_name': self.node_name,
            'game': self.game,
            'mod': default_opts[self.game]['mod'],
            'max_players': self.slots,
            'port': self.port,
            'map': default_opts[self.game]['map']}

        logger.info('options render {}'.format(tpl_data))

        if tools.render_template(
                tpls_dir=self.tpls_dir, tpl='steam_new_node.tpl',
                dst=dst, **tpl_data):
            logger.info('success render template')
            return True
        else:
            logger.critical('failed render template')
            return False
