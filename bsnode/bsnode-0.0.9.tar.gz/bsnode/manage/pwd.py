# -*- coding: utf-8 -*-

import os
import shutil

import svdlib


class PwdManager:
    def __init__(self, node_name):
        self.node_name = node_name
        self.server = svdlib.Supervisor()
        self.status = self.server.status(self.node_name)
        self.node_init_config = '/etc/supervisor/conf.d/{}.conf'.format(
            node_name)

    def exists(self):
        if os.path.exists('/home/{}'.format(self.node_name)):
            # todo: check supervisor
            return True
        else:
            return False

    def start(self):
        node_init_config_off = '{}.off'.format(self.node_init_config)

        if not os.path.exists(node_init_config_off):
            # todo: check supervisor
            return False

        shutil.move(node_init_config_off, self.node_init_config)
        self.server.reread()
        r = self.server.add(self.node_name)
        if r['result']:
            return True
        else:
            return False

    def stop(self):
        node_init_config_off = '{}.off'.format(self.node_init_config)
        if os.path.exists(node_init_config_off):
            # todo: check supervisor
            return True

        r = self.server.stop(self.node_name)
        if r['result']:
            self.server.remove(self.node_name)
            shutil.move(self.node_init_config, node_init_config_off)
            return True
        else:
            return False

    def restart(self):
        r = self.server.restart(self.node_name)
        if r['result']:
            return True
        else:
            return False
