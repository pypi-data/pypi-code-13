# coding=utf-8

import os
import sys
import argparse
import importlib

from monstro.utils.imports import import_object
from monstro.core.constants import SETTINGS_ENVIRONMENT_VARIABLE


def manage():
    argparser = argparse.ArgumentParser()

    argparser.add_argument('command')
    argparser.add_argument('args', nargs='*')
    argparser.add_argument('-s', '--settings')
    argparser.add_argument('-p', '--python-path')

    args = argparser.parse_args()

    if args.settings:
        os.environ[SETTINGS_ENVIRONMENT_VARIABLE] = args.settings

    if args.python_path:
        sys.path.insert(0, args.python_path)

    module_path = 'monstro.management.commands.{}.execute'.format(args.command)

    try:
        import_object(module_path)()
    except (ImportError, TypeError):
        raise AttributeError('Command not found')
