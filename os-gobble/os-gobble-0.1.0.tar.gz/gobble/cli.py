"""Command line interface for Gobble"""

from click import command

from gobble.fiscal import FiscalDataPackage


@command
def validate(file):
    package = FiscalDataPackage(file)
    package.validate(raise_error=False)