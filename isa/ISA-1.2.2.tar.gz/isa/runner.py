#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function, absolute_import

import argparse
import signal

import importlib
import sys
import logging

from isa import __version__
from isa.ini import parse_nodes
from isa.monitor import Monitor
from isa.output import OutputHandler
import sys

__author__ = "Kevin Jacobs"
__copyright__ = "Kevin Jacobs"
__license__ = "MIT"

_logger = logging.getLogger(__name__)
output_types = ['csv', 'standard_output']


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
        help="Set verbosity",
        action='count',
    )
    parser.add_argument(
        '-o',
        '--out',
        '--output',
        dest="output",
        help="Path to output file (possible extensions: .csv)"
    )
    parser.add_argument(
        '-t',
        '--timeout',
        dest="timeout",
        type=int,
        help="Server connect timeout (in seconds)",
        default=5
    )
    parser.add_argument(
        '-i',
        '--interval',
        dest="interval",
        type=int,
        help="Interval for collecting statistics (in seconds)",
        default=5
    )
    parser.add_argument(
        '-p',
        '--plugins',
        dest="plugins",
        help="Comma separated list of plugins (for example 'collectl')",
        default="collectl"
    )
    parser.add_argument(
        '-il',
        '--interlogin',
        dest="interlogin",
        type=int,
        help="The time between two consecutive logins (in seconds), increase when it is not possible to connect to all the nodes at once",
        default=0
    )
    parser.add_argument(
        '-m',
        '--max-nodes',
        dest="max_nodes",
        type=int,
        help="The maximum number of nodes that can login simultaneously",
        default=1
    )
    parser.add_argument(
        '-f',
        '--force',
        dest="force",
        help="Force to recreate the output file",
        action='store_true',
        default=False
    )
    parser.add_argument(
        '-ot',
        '--out-type',
        '--output-type',
        dest="output_type",
        help="The type of the output (should be one of the following: %s)" % output_types,
        default='standard_output'
    )
    return parser.parse_args(args)


def main(args):
    args = parse_args(args)
    output = args.output

    # Set the loglevel
    loglevel = logging.INFO
    if args.loglevel is not None and args.loglevel >= 2:
        loglevel = logging.DEBUG

    logging.basicConfig(level=loglevel, stream=sys.stdout)

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
            _logger.info("Loading plugin_%s" % plugin_name)
            plugin_module = importlib.import_module("plugin_%s" % plugin_name)
        except ImportError:
            try:
                _logger.info("Import failed, trying importing isa.plugin_%s" % plugin_name)
                plugin_module = importlib.import_module("isa.plugin_%s" % plugin_name)
            except ImportError:
                raise Exception("Plugin %s could not be found" % plugin_name)
        plugin = plugin_module.plugin_init(args)
        plugins[plugin_name] = plugin

    # Backward compatibility
    if args.output is not None and args.output.lower()[-4:] == '.csv':
        args.output_type = 'csv'

    if args.output_type not in output_types:
        raise Exception('Output type [%s] is not supported, should be one of the following: %s' % (args.output_type, output_types))

    _logger.info("Output type: %s" % args.output_type)

    output_handler = OutputHandler(output, args.output_type, args.force)
    monitor = Monitor(nodes, args.interval, args.timeout, output_handler.process, plugins, args.interlogin, args.max_nodes)
    monitor.run()


def run():
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
