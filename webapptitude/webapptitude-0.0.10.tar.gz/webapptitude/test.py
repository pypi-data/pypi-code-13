#!/usr/bin/env python

"""
Thin wrapper around unittest to fix up the AppEngine environment and coordinate
test loaders.
"""

import argparse
import unittest
import sys
import os


def fix_cloud_sdk_path(testpath):
    """
    The Google Cloud SDK installation of AppEngine places a separate
    executable dev_appserver.py in a bin/ directory. IT'S A TRAP!!!

    The correct one resides, in that case, in a separate directory...
    """
    if ('google-cloud-sdk/bin' in testpath):
        testpath = testpath.replace('/bin/', '/platform/google_appengine/')
    return testpath


def find_file_in_paths(filename, pathbase=None):
    if pathbase is None:
        pathbase = sys.path
    if os.path.isfile(filename):  # perhaps a full path
        yield filename
    for p in pathbase:
        p = os.path.join(p, filename)
        # print >>sys.stderr, ("Checking path %r" % (p))
        if os.path.isfile(p):
            yield p


def find_executable(name):
    pathbase = os.environ.get('PATH', '').split(':')
    pathbase = [p.strip('"') for p in pathbase]
    for p in find_file_in_paths(name, pathbase=pathbase):
        p = fix_cloud_sdk_path(p)
        if os.access(p, os.X_OK):
            return p  # return the first one
    return None  # not found


def fix_appengine_sys_path(noisy=True):
    sdk_path = find_executable("dev_appserver.py")
    sdk_path = sdk_path and os.path.dirname(sdk_path)
    if (sdk_path is not None):
        # Nesting this allows the test module to import multiple times safely.
        if (sdk_path not in sys.path):
            sys.path.insert(0, sdk_path)
            import dev_appserver
            dev_appserver.fix_sys_path()
    elif noisy:
        message = 'Could not find "dev_appserver.py" (%r)'
        raise ValueError(message % (sdk_path,))


def fix_paths(test_paths=None):
    fix_appengine_sys_path()

    if isinstance(test_paths, list):
        sys.path[:0] = test_paths

    try:
        import appengine_config
        print >>sys.stderr, "Executing appengine_config via test runner."
        (appengine_config)  # evaluate the config.
    except ImportError:
        print "No appengine_config could be imported."


def prepare_test_suite(top_level_dir, pattern, *dirs):
    # Load the tests...
    loader = unittest.loader.TestLoader()
    suiteAll = unittest.TestSuite()

    for testpath in dirs:
        suite = loader.discover(testpath,
                                pattern=(pattern or 'test_*.py'),
                                top_level_dir=top_level_dir)
        suiteAll.addTests(list(suite))

    return suiteAll


def perform_test_suite(suite, args):
    options = dict(
        verbosity=args.verbosity,
        failfast=args.failfast
    )
    return unittest.TextTestRunner(**options).run(suite)


def start_tests(args):
    top_level_dir = args.top_level or os.getcwd()

    os.environ['SERVER_SOFTWARE'] = 'Development/TEST'

    # Start coverate support
    activate_coverage = args.coverage
    if activate_coverage:
        import coverage
        cov = coverage.coverage(timid=False, branch=True)
        cov.start()

    suite = prepare_test_suite(top_level_dir, args.pattern, *args.dirs)
    result = perform_test_suite(suite, args)

    # End coverage support
    if activate_coverage:
        cov.stop()
        cov.save()

    return result.wasSuccessful()


def expose_path(args=None):
    fix_paths()
    return "PYTHONPATH=\"%s\"" % (':'.join(sys.path))

def run_tests(args):
    fix_paths([args.top_level or os.getcwd()] + args.dirs)
    return start_tests(args)



def parse_options(args):
    parser = argparse.ArgumentParser(description="AppEngine Unit Test Runner")

    parser.add_argument('-t', dest='top_level', action='store', default=None)

    parser.add_argument('-v', '--verbosity', action="count",
                        help="increase verbosity", default=1)

    parser.add_argument('-f', '--failfast', action='store_true',
                        help='Quit on first failure', default=False)

    parser.add_argument('--coverage', action='store_true',
                        help="Activate test coverage")

    parser.add_argument('-P', '--pattern', action="store", default=None)

    parser.add_argument('dirs', nargs='+', metavar='path')


    _args = parser.parse_args(args[1:])
    return _args


def main(args=None):
    if args is None:
        args = sys.argv
    success = run_tests(parse_options(args))
    if success:
        sys.exit(0)
    else:
        sys.exit(181)


if __name__ == '__main__':
    main(sys.argv)
