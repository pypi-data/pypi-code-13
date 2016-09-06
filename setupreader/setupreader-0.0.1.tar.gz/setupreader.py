import imp
import json
import functools
import argparse

import mock


def _setup(target, *args, **kwargs):
    target.result = dict(*args, **kwargs)


def load(path):
    setupdict = argparse.Namespace(result=None)

    with mock.patch('setuptools.setup', functools.partial(_setup, setupdict)):
        imp.load_source('packagesetup', path)

    return setupdict.result


def main():
    p = argparse.ArgumentParser(description="Read data from setup.py.")
    p.add_argument('path', help="path to setup.py")
    args = p.parse_args()

    print json.dumps(load(args.path), indent=4)


if __name__ == '__main__':
    main()
