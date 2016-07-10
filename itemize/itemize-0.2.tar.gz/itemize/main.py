#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import logging
import os
import signal
import stat
import sys
from argparse import ArgumentParser
from .document import Document

logger = logging.getLogger(__name__)

def parse_arguments():
    # Parse arguments.
    parser = ArgumentParser(description='Create data-driven receipts.')
    parser.add_argument('filename', nargs='?', default=None,
        help='Path to a JSON-formatted file that specifies document form data.')
    parser.add_argument(
        '-t', '--template', dest='template_name', action='store',
        default='receipt', help='set template name (default: receipt)')
    parser.add_argument(
        '-o', '--output', dest='output_filename', action='store',
        default='output.pdf', help='set template name (default: output.pdf)')
    parser.add_argument(
        '-d', '--log', dest='loglevel', action='store', default='ERROR',
        help=(
            'set log level [DEBUG, INFO, WARNING, ERROR, CRITICAL] '
            '(default: ERROR)'))
    parser.add_argument(
        '--debug', dest='debug', action='store_true', default=False,
        help='run in DEBUG mode')
    args = parser.parse_args()

    if args.debug:
        args.loglevel = 'DEBUG'

    # Configure logger.
    numeric_level = getattr(logging, args.loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % args.loglevel.upper())
    logging.basicConfig(level=numeric_level)

    return args


def sigint_handler(signal, frame):
    sys.exit()


def main():
    # Register SIGINT (Ctrl-C) handler.
    signal.signal(signal.SIGINT, sigint_handler)

    args = parse_arguments()
    logger.debug('Parsed arguments: %s' % args)

    # Support relative file loading using ~ shortcut.
    filename, relative_path = 'stdin', None
    if args.filename:
        absolute_path = os.path.abspath(os.path.expanduser(args.filename))
        relative_path = os.path.join(
            '.', os.path.relpath(absolute_path, os.getcwd()))
        filename = os.path.basename(relative_path)

    # Load JSON input.
    json_input = {}
    try:
        logger.debug('Opening input file (%s).' % relative_path)
        json_file = open(relative_path)
    except IOError as e:
        sys.exit('Could not open input file (%s).\nExiting...' % relative_path)
    except TypeError as e:
        # If stdin is not piped or redirected, display a prompt.
        logger.debug('Reading from stdin.')
        mode = os.fstat(sys.stdin.fileno()).st_mode
        if not (stat.S_ISFIFO(mode) or stat.S_ISREG(mode)):
            print('Reading from stdin. Use Ctrl-D to denote end-of file:')
        json_input = sys.stdin.read()
    else:
        logger.debug('Reading input file (%s).' % relative_path)
        json_input = json_file.read()
        logger.debug('Closing input file (%s).' % relative_path)
        json_file.close()

    # Parse loaded JSON.
    try:
        json_data = json.loads(json_input)
    except ValueError as e:
        sys.exit(
            'Could not parse %s! Check that the input is in a valid JSON '
            'format: %s\nExiting...' % (filename, str(e)))

    # Render and print a PDF document.
    document = Document(template_name=args.template_name, data=json_data)
    document.save(args.output_filename)
    document.print()


if __name__ == '__main__':
    main(sys.argv[1:])
