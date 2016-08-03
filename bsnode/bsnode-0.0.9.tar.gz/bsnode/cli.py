# -*- coding: utf-8 -*-

import click

from bsnode.entry import entry

verbose_console_option = click.option(
    '--verbose-console', help='print message on console', is_flag=True,
    default=False)


@click.group()
def cli():
    pass


@cli.command(short_help='make a node')
@verbose_console_option
@click.argument('node-name')
@click.argument('game')
@click.argument('slots', type=int)
@click.option('--token', help='token for CS: GO and TF2')
def make(node_name, game, slots, verbose_console, token):
    """ BS node maker utility """

    if token:
        opts = {'make': {'node_name': node_name, 'game': game, 'slots': slots,
                         'token': token},
                'verbose_console': verbose_console}
    else:
        opts = {'make': {'node_name': node_name, 'game': game, 'slots': slots},
                'verbose_console': verbose_console}

    return entry(**opts)


@cli.command()
@verbose_console_option
@click.argument('node_name')
def stop(node_name, verbose_console):
    """ stop node """
    return entry(**{'stop': {'node_name': node_name},
                    'verbose_console': verbose_console})


@cli.command()
@verbose_console_option
@click.argument('node_name')
def start(node_name, verbose_console):
    """ start node """
    return entry(**{'start': {'node_name': node_name},
                    'verbose_console': verbose_console})


@cli.command()
@verbose_console_option
@click.argument('node_name')
def restart(node_name, verbose_console):
    """ restart node """
    return entry(**{'restart': {'node_name': node_name},
                    'verbose_console': verbose_console})


@cli.command()
@verbose_console_option
@click.argument('node_name')
def remove(node_name, verbose_console):
    """ remove node """
    return entry(**{'remove': {'node_name': node_name},
                    'verbose_console': verbose_console})
