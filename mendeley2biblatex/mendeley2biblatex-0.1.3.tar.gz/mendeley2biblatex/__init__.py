import sys
from argparse import ArgumentParser

from mendeley2biblatex.library_converter import LibraryConverter


__all__ = ["bib_entry", "library_converter"]


def main():
    """Set this script some command line options. See usage."""

    parser = ArgumentParser(description='Convert a sqlite database from mendeley to bibetex')
    # usage: %prog [-o out.bib] mendeley.sqlite''', version='%prog ' + version)

    parser.add_argument('-q', '--quiet', action='store_true', default=False,
        dest='quiet', help='Do not display any information.')
    parser.add_argument('-f', '--folder', default=None,
        dest='folder', help='Limit output to mendeley folder')
    parser.add_argument("-o", "--output", dest="bibtex_file", default=sys.stdout,
        help="BibTeX file name, else output will be printed to stdout")
    parser.add_argument('input', metavar='INPUT_FILE', nargs='?',
        help='the mendeley database')

    args = parser.parse_args()

    if not args.input:
        parser.error('''No file specified''')

    LibraryConverter.convert_library(args.input, args.bibtex_file, args.quiet, args.folder)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted by user')
