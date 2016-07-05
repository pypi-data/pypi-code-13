"""Handles the CLI (Command line interface)"""

import sys
import os

import argparse

from psclient import connect
import json
import pprint

from psclient.manager_client import SystemCacheConfiguration

def main():
    p = argparse.ArgumentParser(description="Predictive Service client")
    p.add_argument('--manager-endpoint',
        help="The manager endpoint URL for the predictive service")
    p.add_argument('--admin-key',
        help="The admin key to use")
    p.add_argument('--config',
        help="The config file to use")


    sp = p.add_subparsers(title="commands")

    get_status_sp = sp.add_parser('get_status')
    get_status_sp.set_defaults(func=get_status)
    get_status_sp.add_argument('--cache', action='store_true')
    get_status_sp.add_argument('--node', action='store_true')
    get_status_sp.add_argument('--endpoint', action='store_true')

    get_system_cache_configuration_sp = sp.add_parser('get_system_cache_configuration')
    get_system_cache_configuration_sp.set_defaults(func=get_system_cache_configuration)

    update_system_cache_configuration_sp = sp.add_parser('update_system_cache_configuration')
    update_system_cache_configuration_sp.set_defaults(func=update_system_cache_configuration)

    for attr in SystemCacheConfiguration.__rest__:
        update_system_cache_configuration_sp.add_argument(
            "--"+attr,
            help="The "+attr,
            default=argparse.SUPPRESS)


    clear_cache_sp = sp.add_parser('clear_cache')
    clear_cache_sp.set_defaults(func=clear_cache)

    args = p.parse_args()

    args.predictive_service = connect(
        config_file=args.config,
        manager_endpoint=args.manager_endpoint,
        admin_key=args.admin_key)

    args.func(args)

def get_status(args):
    if args.cache:
        view = 'cache'
    elif args.node:
        view = 'node'
    elif args.endpoint:
        view = 'endpoint'
    else:
        view = None
    pprint.pprint(args.predictive_service.get_status(view=view))

def get_system_cache_configuration(args):
    pprint.pprint(args.predictive_service.get_system_cache_configuration())

def update_system_cache_configuration(args):
    from psmanager_client import SystemCacheConfiguration

    system_cache_configuration = args.predictive_service.get_system_cache_configuration()

    for attr in SystemCacheConfiguration.__rest__:
        # Replace the value if specified.
        setattr(system_cache_configuration, attr,
            getattr(args, attr,
                getattr(system_cache_configuration, attr)))

    pprint.pprint(args.predictive_service.update_system_cache_configuration(system_cache_configuration))

def clear_cache(args):
    pprint.pprint(args.predictive_service.clear_cache())
