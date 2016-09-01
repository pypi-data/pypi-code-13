from linkfinder.source import SimpleDirectorySource
from linkfinder.driver import GeventDriver
from linkfinder.runner import get_runner
import argparse
import sys


def execute():
    parser = argparse.ArgumentParser(description='Finds links and checks them.')
    parser.add_argument('--dir', dest='dir', help='Provide the path to a directory')
    args = parser.parse_args()

    if not args.dir:
        parser.print_help()
        sys.exit(2)

    # init
    directory = args.dir
    driver = GeventDriver()
    source = SimpleDirectorySource(directory)

    # run
    runner = get_runner(driver=driver, source=source)
    runner.run()
    runner.print_results()
