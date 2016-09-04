#!/usr/bin/env python
# coding=utf-8

from __future__ import print_function

from argparse import ArgumentParser

from termcolor import colored

from versiontracker import iter_version_info, supported_software
from versiontracker._version import __version__


def _colored_product(product):
    return colored(product, attrs=["bold"])


def _print_product(data):
    formatted_data = {
        'product': _colored_product(data["id"]),
        'version': colored(data["version"], "green"),
        'url': colored(data["url"], "magenta"),
    }
    template = u"{product}: {version} @ {url}"
    if "date" in data and data["date"]:
        formatted_data['date'] = colored(
            data["date"].strftime(u"%Y-%m-%d"), "cyan")
        template = u"{product}: {version} ({date}) @ {url}"
    print(template.format(**formatted_data))


def main():
    parser = ArgumentParser(
        description=u"Prints the latest stable version, release date and "
                    u"reference URL of the specified software products.")
    parser.add_argument(
        'products', nargs='*', metavar='product', default=supported_software(),
        help=u"ID of a software product whose latest stable version you want "
             u"to know. Use -l to get a list of available IDs. If omitted, "
             u"all supported products are selected.")
    parser.add_argument(
        '-l', '--list-ids', action='store_true', dest='list_ids',
        help=u"Lists IDs of supported software products.")
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s {}'.format(__version__))
    options = parser.parse_args()
    if options.list_ids:
        for product in supported_software():
            print(_colored_product(product))
    else:
        for data in iter_version_info(options.products):
            _print_product(data)
