# -*- coding: utf-8 -*-
import codecs
import logging
import os
import pkg_resources

from alchy import Manager
import click
import yaml

from approved import __title__, __version__
from approved.store.models import Model

log = logging.getLogger(__name__)


class EntryPointsCLI(click.MultiCommand):

    """Add subcommands dynamically to a CLI via entry points."""

    def _iter_commands(self):
        """Iterate over all subcommands as defined by the entry point."""
        return {entry_point.name: entry_point for entry_point in
                pkg_resources.iter_entry_points('approved.subcommands.1')}

    def list_commands(self, ctx):
        """List the available commands."""
        commands = self._iter_commands()
        return commands.keys()

    def get_command(self, ctx, name):
        """Load one of the available commands."""
        commands = self._iter_commands()
        if name not in commands:
            click.echo("no such command: {}".format(name))
            ctx.abort()
        return commands[name].load()


@click.group(cls=EntryPointsCLI)
@click.option('-c', '--config', default='~/.approved.yaml',
              type=click.Path(), help='path to config file')
@click.option('-d', '--database', help='path/URI of the SQL database')
@click.option('-l', '--log-level', default='INFO')
@click.option('-r', '--reset', is_flag=True,
              help='reset database from scratch')
@click.option('--log-file', type=click.Path())
@click.version_option(__version__, prog_name=__title__)
@click.pass_context
def root(context, config, database, reset, log_level, log_file):
    """Interact with Taboo genotype comparison tool."""
    log.info("{}: version {}".format(__title__, __version__))

    # read in config file if it exists
    if os.path.exists(config):
        with codecs.open(config) as conf_handle:
            context.obj = yaml.load(conf_handle)
    else:
        context.obj = {}

    if context.invoked_subcommand != 'serve':
        # setup database
        uri = database or context.obj.get('database') or 'sqlite://'
        if '://' not in uri:
            # guess it's a path to SQLite database
            uri = "sqlite:///{}".format(uri)
        config = dict(SQLALCHEMY_DATABASE_URI=uri)
        context.obj['db'] = Manager(config=config, Model=Model)

        if reset:
            context.obj['db'].drop_all()
        context.obj['db'].create_all()
