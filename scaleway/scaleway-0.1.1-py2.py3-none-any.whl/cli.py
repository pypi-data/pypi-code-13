# -*- coding: utf-8 -*-
# Copyright 2016 Antoni Segura Puimedon <celebdor@gmail.com>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import getpass
import logging
import os
import subprocess
import sys

from scaleway import utils
import click

LOG = logging.getLogger()


@click.group()
def cli():
    pass


@click.command(help='Shows the ip of the machine')
@click.option('--machine', default='devstack', help='name of the machine to '
              'show the public IP address for.')
@click.option('--token', default=None,
              help='scaleway API token. If not provided, will try to retrieve '
              'it with unix `pass` at the path indicated by the env var'
              '$SCALEWAY_PASS_PATH.')
def show(machine, token):
    if token is None:
        pass_path = os.environ.get('SCALEWAY_PASS_PATH')
        if pass_path is None:
            LOG.error('Either a token option must be provided or the '
                      '$SCALEWAY_PASS_PATH env var must be defined')
            sys.exit(1)
        token = utils.get_scaleway_token(pass_path)

    print(utils.get_ip(machine, token))


@click.command(help='ssh mounts the machine')
@click.option('--machine', default='devstack', help='name of the machine to '
              'retrieve')
@click.option('--token', default=None,
              help='scaleway API token. If not provided, will try to retrieve '
              'it with unix `pass` at the path indicated by the env var'
              '$SCALEWAY_PASS_PATH.')
def mount(machine, token):
    if token is None:
        pass_path = os.environ.get('SCALEWAY_PASS_PATH')
        if pass_path is None:
            LOG.error('Either a token option must be provided or the '
                      '$SCALEWAY_PASS_PATH env var must be defined')
            sys.exit(1)
        token = utils.get_scaleway_token(pass_path)

    ip = utils.get_ip(machine, token)

    mount_dir = os.path.join(os.environ.get('HOME'), 'mnt', machine)
    LOG.info('Checking mount destination "%s" existence...', mount_dir)
    os.makedirs(mount_dir, exist_ok=True)

    LOG.info('sshfs mounting...')
    subprocess.check_call([
        'sshfs',
        '%(username)s@%(ip)s:/home/%(username)s' % {
            'username': getpass.getuser(),
            'ip': ip},
        mount_dir,
        '-o',
        'compression=yes'])
    LOG.info('mounted!')


@click.command(help='ssh unmounts the machine')
@click.option('--machine', default='devstack', help='name of the machine to '
              'umount')
def umount(machine):
    mount_dir = os.path.join(os.environ.get('HOME'), 'mnt', machine)
    try:
        subprocess.check_output([
            'findmnt',
            '--mountpoint',
            mount_dir])
    except subprocess.CalledProcessError:
        LOG.info('ssh mount point "%s" not among fuser mounts', mount_dir)
    else:
        LOG.info('fuser umounting...')
        subprocess.check_call([
            'fusermount',
            '-u',
            mount_dir])
        LOG.info('umounted!')


cli.add_command(mount)
cli.add_command(show)
cli.add_command(umount)


def main():
    handler = logging.StreamHandler(sys.stderr)
    LOG.setLevel(logging.INFO)
    LOG.addHandler(handler)
    cli()
