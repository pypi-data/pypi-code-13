#
# Copyright (c) 2016, Michael Conroy
#


import sys
import argparse


from ..interface import Tool
from ..loaders import StringLoader
from validation import SimpleCSVFileValidator


class SimpleCSVValidationTool(Tool):
    """  Defines available/callable validation tool to CLI """

    name = 'simple-validator'
    arguments = [
        (
            'filename',
            {'type': argparse.FileType('r')},
            {'help': 'The file containing the structure to validate.'},
        ),
        (
            '--headers',
            {'nargs': '+'},
            {'help': 'A list detailing the expected headers'},
        ),
    ]
    description = 'CLI tool for validating CSVs'

    def implementation(self, *args, **kwargs):
        validation = SimpleCSVFileValidator(StringLoader(self.args.filename))
        validation.set_validators(self.args.headers)
        if validation.validate():
            sys.stdout.write(validation.log)
            return 0
        else:
            sys.stderr.write(validation.log)
            return 1
