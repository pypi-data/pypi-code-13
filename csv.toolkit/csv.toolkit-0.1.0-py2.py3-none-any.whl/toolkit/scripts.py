#
# Copyright (c) 2016, Michael Conroy
#


import sys
import argparse
import pkg_resources


from interface import Tool


class CSVToolsCLIScript(object):
    """ CLI entry point """

    def __init__(self):
        self.avail_tools = Tool.mapped()
        avail_tool_names = self.avail_tools.keys()

        self.parser = argparse.ArgumentParser()

        try:
            self_version = \
                pkg_resources.get_distribution('csvtools').version
        except pkg_resources.DistributionNotFound:  # pragma: no cover
            self_version = 'UNKNOWN'
        self.parser.add_argument(
            '-v',
            '--version',
            action='version',
            version='%(prog)s ' + self_version,
        )

        self.parser.add_argument(
            'tool',
            choices=avail_tool_names,
            help='The name of the desired tool.',
        )

    def __call__(self, *args, **kwargs):
        arguments = self.parser.parse_known_args()
        tool = arguments[0].tool
        leftovers = arguments[1]
        tool_instance = self.avail_tools[tool](*leftovers)
        sys.exit(tool_instance())


main = CSVToolsCLIScript()
