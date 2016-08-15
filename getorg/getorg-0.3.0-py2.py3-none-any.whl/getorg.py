"""Code for standalone file"""


def getorg_standalone():
    """
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('org', help='pypi package name', nargs='+')
    parser.add_argument('-q',
                        '--quiet',
                        help='no output',
                        action='store_true')
    parser.add_argument('-j',
                        '--json',
                        help='use pypi json api instead of xmlrpc',
                        action='store_true')
    parser.add_argument('-p',
                        '--pattern',
                        help='only show files matching a regex pattern')
    args = parser.parse_args()
    packages = args.package
    verbose = not (args.quiet)
    version = None
    grand_total = 0
    package_list = []
    json = args.json


if __name__ == '__main__':
    getorg_standalone()
