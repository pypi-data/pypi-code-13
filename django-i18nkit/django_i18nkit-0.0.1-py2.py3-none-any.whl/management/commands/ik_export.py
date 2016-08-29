from django.core.management import BaseCommand

from i18nkit.excel import write_catalog_workbook
from i18nkit.utils import merge_catalog_files


class Command(BaseCommand):
    def add_arguments(self, parser):
        """
        :type parser: argparse.ArgumentParser
        """
        parser.add_argument('-i', '--input', nargs='*')
        parser.add_argument('-o', '--output')

    def handle(self, input, output, **options):
        merged_catalog = merge_catalog_files(input)
        if output.endswith('xlsx'):
            with open(output, 'wb') as outfp:
                write_catalog_workbook(outfp, merged_catalog)
                self.stdout.write('Wrote: %s' % outfp.name)
        else:  # pragma: no cover
            raise ValueError('unknown output type: %s' % output)
