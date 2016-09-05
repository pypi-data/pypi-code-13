import os

from babel.messages import Catalog
from babel.messages.extract import check_and_call_extract_file, DEFAULT_KEYWORDS
from babel.messages.pofile import write_po
from django.core.management import BaseCommand

from i18nkit.jinja2_extract import jinja2_extract
from i18nkit.utils import add_paths_options, DirectoryFilter, get_paths

METHOD_MAP = [
    ('**.js', 'javascript'),
    ('**.py', 'python'),
    ('**/templates/**.html', 'django'),
    ('**/templates/**.jinja', jinja2_extract),
]

OPTIONS_MAP = {
    '**/templates/**.jinja': {'newstyle_gettext': 'true'},
}

KEYWORDS = dict(DEFAULT_KEYWORDS.copy())
for kw in set(kw for kw in KEYWORDS if kw.isalpha()):
    KEYWORDS['%s_lazy' % kw] = KEYWORDS[kw]


def extract_from_dir(dirname, method_map, options_map, keywords, dirname_filter=None, status_callback=None):
    absname = os.path.abspath(dirname)
    for root, dirnames, filenames in os.walk(absname):
        if dirname_filter:
            dirnames[:] = [dirname for dirname in dirnames if dirname_filter(os.path.join(root, dirname))]
        dirnames.sort()
        filenames.sort()
        for filename in filenames:
            filepath = os.path.join(root, filename).replace(os.sep, '/')

            for message_tuple in check_and_call_extract_file(
                filepath,
                method_map=method_map,
                options_map=options_map,
                callback=status_callback,
                keywords=keywords,
                dirpath=absname,
                comment_tags=(),
                strip_comment_tags=False,
            ):
                yield message_tuple


class Command(BaseCommand):
    def add_arguments(self, parser):
        """
        :type parser: argparse.ArgumentParser
        """
        parser.add_argument('-o', '--output')
        add_paths_options(parser)
        DirectoryFilter.add_options(parser)
        parser.add_argument('-H', '--omit-header', action='store_true')
        parser.add_argument('-z', '--zero-lineno', action='store_true')

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
        catalog = self.build_catalog(paths)
        self.write_catalog(catalog)

    def write_catalog(self, catalog):
        output_path = self.config['output']
        if not output_path:
            self.stdout.write('would write POT with %d entries, but no `-o` given' % len(catalog))
            return
        self.stdout.write('writing POT with %d entries to %s' % (len(catalog), output_path))
        with open(output_path, 'wb') as outfile:
            write_po(
                outfile,
                catalog,
                width=0,
                omit_header=self.config['omit_header'],
                sort_output=True
            )

    def build_catalog(self, paths):
        catalog = Catalog(charset='UTF-8')
        for path in sorted(paths):
            if self.config['verbosity'] > 1:
                self.stdout.write('processing %s' % path)
            extracted = extract_from_dir(
                path,
                method_map=METHOD_MAP,
                options_map=OPTIONS_MAP,
                keywords=KEYWORDS,
                status_callback=self.status_callback,
                dirname_filter=self.dirname_filter,
            )

            for filename, lineno, message, comments, context in extracted:
                filepath = os.path.normpath(os.path.join(path, filename))
                if self.config['zero_lineno']:
                    lineno = 0

                catalog.add(message, None, [(filepath, lineno)], auto_comments=comments, context=context)
        return catalog

    def status_callback(self, filename, method, options):
        if self.config['verbosity'] > 2:
            self.stdout.write('... %s: %s (%s)' % (filename, method, options))
