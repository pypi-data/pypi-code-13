import os

from babel.messages.pofile import read_po, write_po
from django.conf import settings
from django.core.management import BaseCommand

from i18nkit.excel import read_catalog_workbook
from i18nkit.utils import merge_catalogs


class Command(BaseCommand):
    def add_arguments(self, parser):
        """
        :type parser: argparse.ArgumentParser
        """
        parser.add_argument('-i', '--input')
        parser.add_argument('-o', '--output-template')
        parser.add_argument('-s', '--source-language', default=settings.LANGUAGES[0][0])

    def handle(self, input, output_template, source_language, **options):
        if input.endswith('xlsx'):
            with open(input, 'rb') as infp:
                catalogs = read_catalog_workbook(infp)
        else:  # pragma: no cover
            raise ValueError('unknown input type: %s' % input)

        for locale, update_catalog in sorted(catalogs.items()):
            if locale == source_language:
                continue
            self.write_updated_catalog(output_template, update_catalog)

    def write_updated_catalog(self, output_template, update_catalog):
        locale = str(update_catalog.locale)
        if output_template:
            output_filename = os.path.abspath(output_template.replace('{locale}', locale))
            output_dir = os.path.dirname(output_filename)
            if not os.path.isdir(output_dir):
                os.makedirs(output_dir)
        else:
            output_filename = None

        # Start with the template catalog,

        if output_filename and os.path.isfile(output_filename):
            with open(output_filename, 'rb') as infp:
                existing_catalog = read_po(infp, locale)
        else:
            existing_catalog = None

        # merge them in,
        catalog = merge_catalogs([existing_catalog, update_catalog])

        # And prune translationless entries
        for msg in list(catalog):
            if not msg.string:
                catalog.delete(msg.id)

        if output_filename:
            # and write things out
            with open(output_filename, 'wb') as outfp:
                write_po(outfp, catalog, width=0, sort_output=True, omit_header=True)
            self.stdout.write('Wrote %d entries in %s to %s' % (len(catalog), catalog.locale, output_filename))
        else:
            self.stdout.write('Would have written %d entries in %s' % (len(catalog), catalog.locale))
