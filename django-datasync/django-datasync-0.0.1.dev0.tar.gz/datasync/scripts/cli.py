# Skeleton of a CLI

import click

import datasync


@click.command('datasync')
@click.argument('count', type=int, metavar='N')
def cli(count):
    """Echo a value `N` number of times"""
    for i in range(count):
        click.echo(datasync.has_legs)
