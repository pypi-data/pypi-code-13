"""Module describing the planemo ``ci_find_repos`` command."""
from __future__ import print_function

import click

from planemo import options
from planemo.cli import command_function
from planemo.shed import find_raw_repositories


@click.command('ci_find_repos')
@options.shed_project_arg()
@command_function
def cli(ctx, paths, **kwds):
    """Find all shed repositories in one or more directories.

    Currently, a shed repository is considered a directory with a .shed.yml
    file.
    """
    kwds["recursive"] = True
    repos = find_raw_repositories(ctx, paths, **kwds)
    print(repos)
