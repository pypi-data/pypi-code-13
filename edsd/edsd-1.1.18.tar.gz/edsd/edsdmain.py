#!/usr/local/python
# coding:utf-8
# Copyright (C) Alibaba Group

"""
EDAS detector - A simple script to detect the EDAS running environment.

$ edsd help
  show this document.

$ edsd list [check_id][.point_id]

$ edsd list 1

$ edsd list 1.1

$ edsd check 1

$ edsd check 1.1

$ edsd check all

$ edsd view [check_id.point_id]
"""

__author__ = "Thomas Li <yanliang.lyl@alibaba-inc.com>"
__license__ = "GNU License"

import sys

from edsd import __version__, colored
import edsd.collect

try:
    import warnings
    warnings.filterwarnings("ignore")

    import getpass
    user = getpass.getuser()
    if user != 'admin':
        sys.stderr.write(colored("Warning", 'red') +
                         ": edsd is recommended running with user 'admin'\n")
        import sys
        sys.exit(1)

    import sys
    ver = sys.version_info
    if ver < (2, 6):
        print colored("Warning", 'red') + ': python version needs 2.6+'
except:
    pass


def collect():
    import edsd.collect
    edsd.collect.collect()

def main_shell():
    import edsd.cps
    import edsd.commandline
    cpc = edsd.commandline.CheckPointCmd()
    try:
        edsd.cps.install()
        cpc.cmdloop()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as _:
        import traceback
        traceback.print_exc()

def commandline():
    from optparse import OptionParser
    parser = OptionParser("usage %prog [options] action")
    parser.add_option('-v', '--verbose', dest="verbose", action="store_true",
                      default=False, help="print detail messages.")

    (options, args) = parser.parse_args()

    if options.verbose:
        edsd.collect.DEBUG = True

    if len(args) == 0:
        print parser.get_usage()

    try:
        do(args[0], *args[1:])
    except Exception as e:
        sys.stderr.write(e.message)


def do(name, *args):
    cmd = CommandLine()
    func = getattr(cmd, 'do_'+name, None)
    if func is None:
        raise Exception('no action ("%s") defined.' % name)
    func(*args)


class CommandLine():
    def do_view(self, *args):
        edsd.collect.view(*args)

    def do_version(self, *args):
        print __version__


if __name__ == '__main__':
    commandline()

