import os

from babel.messages import Catalog
from babel.messages.mofile import write_mo
from babel.messages.pofile import read_po
from django.core.management import BaseCommand
from django.utils.six import BytesIO

from i18nkit.utils import add_paths_options, DirectoryFilter, get_paths


class Command(BaseCommand):
    def add_arguments(self, parser):
        """
        :type parser: argparse.ArgumentParser
        """
        add_paths_options(parser)
        DirectoryFilter.add_options(parser)

    def handle(self, **options):
        self.config = options
        self.dirname_filter = DirectoryFilter(
            ignore_dirs=options['ignore_dirs'],
            default_ignore_dirs=options['default_ignore_dirs'],
        )
        paths = get_paths(
            apps=self.config['apps'],
            dirs=self.config['dirs'],
            dir_children=self.config['dir_children'],
            all_apps=self.config['all_apps'],
            dirname_filter=self.dirname_filter,
        )
        for root in paths:
            self.process_dir(root)

    def process_dir(self, root):
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [dirname for dirname in dirnames if self.dirname_filter(os.path.join(root, dirname))]
            for file in filenames:
                if not file.endswith('.po'):
                    continue
                self.process_file(os.path.join(dirpath, file))

    def process_file(self, file):
        outfile = '%s.mo' % os.path.splitext(file)[0]
        try:
            with open(file, 'rb') as infp:
                catalog = read_po(infp)
            out_bio = BytesIO()
            write_mo(out_bio, catalog)
            with open(outfile, 'wb') as outfp:
                outfp.write(out_bio.getvalue())
        except Exception as exc:
            self.stderr.write('could not process %s: %s' % (file, exc))
        else:
            self.stdout.write('compiled %s -> %s' % (file, outfile))
