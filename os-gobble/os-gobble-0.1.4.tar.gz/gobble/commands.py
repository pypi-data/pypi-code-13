"""Command line interface for Gobble"""


from click import command, argument, Path

from gobble.fiscal import FiscalDataPackage


@command(name='check')
@argument('filepath', type=Path(exists=True))
def validate(filepath):
    package = FiscalDataPackage(filepath)
    package.validate(raise_error=False)
