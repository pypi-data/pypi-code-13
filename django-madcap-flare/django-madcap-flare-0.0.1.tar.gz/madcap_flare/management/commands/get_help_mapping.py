"""Turn the MCF .h file into a help mapping and print it out.
"""
from argparse import FileType
from pprint import pformat

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Run the command.
    """

    help = u'Parse an MCF .h file and output a dict.'

    def add_arguments(self, parser):  # pylint: disable=R0201
        """Parse.
        """
        parser.add_argument(
            'header', type=FileType('r'), help='Header file to read from.')

    def handle(self, *args, **options):
        """Run the command.
        """
        content = options['header'].read().replace('\t', ' ')

        lines = content.splitlines()
        data_dict = dict(line.split(' ')[1:3] for line in lines if line)
        output = pformat(data_dict, indent=4)
        output = u'{{\n {out}\n}}'.format(out=output[1:-1])
        self.stdout.write(output)
