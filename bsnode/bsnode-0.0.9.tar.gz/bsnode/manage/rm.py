# -*- coding: utf-8 -*-

import os
import logging
import subprocess

import bsnode.ports
from bsnode.manage.pwd import PwdManager


logger = logging.getLogger(__name__)


def del_user(user):
    command = '/usr/sbin/deluser {} --remove-home'.format(user)
    r = subprocess.call(
        command, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
        shell=True)

    if r != 0:
        logger.critical('deleting user is failure (exit code: {})'.format(r))
        return False

    return True


def rm_node(node_name):
    pwd = PwdManager(node_name)
    del_files = [
        '/var/log/supervisor/{}_err.log'.format(node_name),
        '/var/log/supervisor/{}_out.log'.format(node_name),
        '{}.off'.format(pwd.node_init_config)]

    if not pwd.exists():
        logger.critical('node {} not exists'.format(node_name))
        return False

    logger.info('stopping node...')
    pwd.stop()
    logger.info('deleting files...')
    for item in del_files:
        logger.info('delete {}'.format(item))
        os.remove(item)

    logger.info('deleting user...')
    del_user(node_name)

    logger.info('deleting port...')
    port = bsnode.ports.Ports(node_name)
    port.remove()

    logger.info('node deleted')
    return True
