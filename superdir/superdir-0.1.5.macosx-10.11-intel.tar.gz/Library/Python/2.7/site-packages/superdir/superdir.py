#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys

import click

from tree import Tree
from validator import Validator
import callbacks as cbs
import utils


def main(schema=None, OUTPUT_DIR=None, CONFIG_PATH=None):
    ''' Validate schema file and output directory parameters, build a tree from schema, callback on each node.  '''

    validator = Validator(schema, OUTPUT_DIR=OUTPUT_DIR)
    if not validator.validate():
        click.echo(validator.error['msg'])
        sys.exit(1)

    directory_tree = Tree(
        INDENT_SIZE = validator.INDENT_SIZE,
        OUTPUT_DIR  = OUTPUT_DIR,
        base_path   = os.path.abspath(os.curdir)
    )
    directory_tree.load_data(schema)
    directory_tree.build_tree()

    callbacks = [
        cbs.create_file,
    ]

    if CONFIG_PATH:
        process_hooks = cbs.make_config_processor(CONFIG_PATH)
        callbacks.append(process_hooks)

    directory_tree.walk(callbacks=callbacks)


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.argument('schema_file', type=click.File('r'), required=True, default=sys.stdin)
@click.option('-c', '--config', nargs=1, type=str, help="Path to config file to read before superdir'ing your schema.")
@click.option('-o', '--outfile', nargs=1, type=str, help=("Directory name to contain your superdir'd files. If none is" 
                                                          "supplied, your schema file must have exactly one top-level directory"         
                                                          "and no sibling regular files. That top-level directory will be the"
                                                          "parent of your new file tree. If an output directory is supplied"
                                                          "then any validly-indented schema file is allowed."))
def cli(schema_file, outfile, config):

    schema = None

    if schema_file is None:

        # schema probably coming from a pipe
        if not sys.stdin.isatty():
            schema = list(sys.stdin) 

    else:

        # schema from a file
        schema = list(schema_file)

    main(schema=schema, OUTPUT_DIR=outfile, CONFIG_PATH=config)

if __name__ == '__main__':

    cli()
