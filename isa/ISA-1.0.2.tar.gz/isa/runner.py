#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function, absolute_import

import argparse
import importlib
import sys
import logging

from isa import __version__
from isa.ini import parse_nodes
from isa.monitor import Monitor
from isa.output import OutputHandler

__author__ = "Kevin Jacobs"
__copyright__ = "Kevin Jacobs"
__license__ = "MIT"

_logger = logging.getLogger(__name__)


def parse_args(args):
    """
    Parse command line parameters

    :param args: command line parameters as list of strings
    :return: command line parameters as :obj:`argparse.Namespace`
    """
    parser = argparse.ArgumentParser(
        description="Monitor nodes")
    parser.add_argument(
        '--version',
        action='version',
        version='ISA {ver}'.format(ver=__version__))
    parser.add_argument(
        dest="nodes",
        help="Path to nodes.ini file")
    parser.add_argument(
        '-v',
        '--verbose',
        dest="loglevel",
        help="Set loglevel to INFO",
        action='store_const',
        const=logging.INFO)
    parser.add_argument(
        '-vv',
        '--very-verbose',
        dest="loglevel",
        help="Set loglevel to DEBUG",
        action='store_const',
        const=logging.DEBUG)
    parser.add_argument(
        '-o',
        '--out',
        dest="output",
        help="Path to output file (possible extensions: .csv)"
    )
    parser.add_argument(
        '--timeout',
        dest="timeout",
        type=int,
        help="Server connect timeout (in seconds)",
        default=5
    )
    parser.add_argument(
        '--interval',
        dest="interval",
        type=int,
        help="Interval for collecting statistics (in seconds)",
        default=5
    )
    parser.add_argument(
        '--plugins',
        dest="plugins",
        help="Comma separated list of plugins (for example 'iostat')",
        default="iostat"
    )
    return parser.parse_args(args)


def main(args):
    args = parse_args(args)
    output = args.output
    logging.basicConfig(level=args.loglevel, stream=sys.stdout)
    _logger.debug("Parsed arguments: %s" % args)
    nodes = parse_nodes(args.nodes)
    _logger.debug("Parsed node information: %s" % nodes)
    _logger.info("Starting monitor")

    # Load plugins
    plugin_names = args.plugins.split(",")
    plugins = {}
    for plugin_name in plugin_names:
        _logger.info("Loading plugin %s" % plugin_name)
        try:
            _logger.info("Trying importing plugin_%s" % plugin_name)
            plugin_module = importlib.import_module("plugin_%s" % plugin_name)
        except ImportError:
            try:
                _logger.info("Import failed, trying importing isa.plugin_%s" % plugin_name)
                plugin_module = importlib.import_module("isa.plugin_%s" % plugin_name)
            except ImportError:
                raise Exception("Plugin %s could not be found" % plugin_name)
        plugin = plugin_module.plugin_init(args)
        plugins[plugin_name] = plugin

    output_handler = OutputHandler(output)
    monitor = Monitor(nodes, args.interval, args.timeout, output_handler.process, plugins)
    monitor.run()


def run():
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
