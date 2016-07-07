import click

from .requirements import Requirements

@click.group()
def cli():
    cli.rqr = Requirements()

@cli.command()
def list():
    click.echo(cli.rqr)

@cli.command()
@click.argument('pkg')
@click.option('--save', 'target', flag_value='base')
@click.option('--save-development', 'target', flag_value='development')
@click.option('--save-production', 'target', flag_value='production')
def install(pkg, target = None):
    click.echo(cli.rqr.install(pkg, target))

@cli.command()
def migrate():
    cli.rqr.migrate()
