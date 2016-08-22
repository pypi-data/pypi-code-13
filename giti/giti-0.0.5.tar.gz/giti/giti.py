#!/usr/bin/env python3

import argparse
import errno
import os
import sys
import traceback

import config

# Application version
ver = '0.0.5'

# Default paths to Mercurial and Git
hg_cmd = 'hg'
git_cmd = 'git'


# Logging and output
def log(msg):
    sys.stdout.write(msg)


def message(msg):
    return "[giti] %s\n" % msg


def info(msg, level=1):
    if level <= 0 or verbose:
        for line in msg.splitlines():
            log(message(line))


def action(msg):
    for line in msg.splitlines():
        log(message(line))


def warning(msg):
    for line in msg.splitlines():
        sys.stderr.write("[giti] WARNING: %s\n" % line)
    sys.stderr.write("---\n")


def error(msg, code=-1):
    for line in msg.splitlines():
        sys.stderr.write("[giti] ERROR: %s\n" % line)
    sys.stderr.write("---\n")
    sys.exit(code)


# Process execution
class ProcessException(Exception):
    pass


# Handling for multiple version controls
scms = {}


def scm(name):
    def _scm(cls):
        scms[name] = cls()
        return cls

    return _scm


# Subparser handling
parser = argparse.ArgumentParser(prog='giti',
                                 description="Command-line Git Improve Tool\nversion %s\n\n" % ver +
                                             "Use 'giti <command> -h|--help' for detailed help.\n" +
                                             "Online manual and guide available at https://github.com/xuzhuoyi/giti",
                                 formatter_class=argparse.RawTextHelpFormatter)
subparsers = parser.add_subparsers(title="Commands", metavar="           ")
parser.add_argument("--version", action="store_true", dest="version", help="print version number and exit")
subcommands = {}


# Process handling
def subcommand(name, *args, **kwargs):
    def __subcommand(command):
        if not kwargs.get('description') and kwargs.get('help'):
            kwargs['description'] = kwargs['help']
        if not kwargs.get('formatter_class'):
            kwargs['formatter_class'] = argparse.RawDescriptionHelpFormatter

        subparser = subparsers.add_parser(name, **kwargs)
        subcommands[name] = subparser

        for arg in args:
            arg = dict(arg)
            opt = arg['name']
            del arg['name']

            if isinstance(opt, str):
                subparser.add_argument(opt, **arg)
            else:
                subparser.add_argument(*opt, **arg)

        subparser.add_argument("-v", "--verbose", action="store_true", dest="verbose", help="Verbose diagnostic output")
        subparser.add_argument("-vv", "--very_verbose", action="store_true", dest="very_verbose",
                               help="Very verbose diagnostic output")

        def thunk(parsed_args):
            argv = [arg['dest'] if 'dest' in arg else arg['name'] for arg in args]
            argv = [(arg if isinstance(arg, str) else arg[-1]).strip('-').replace('-', '_')
                    for arg in argv]
            argv = {arg: vars(parsed_args)[arg] for arg in argv
                    if vars(parsed_args)[arg] is not None}

            return command(**argv)

        subparser.set_defaults(command=thunk)
        return command

    return __subcommand


# New command
@subcommand('down',
            dict(name='url', help='Git repo url'),
            dict(name=['-p', '--proxy'], action='store_true', help='Use proxy to clone the repository.'),
            dict(name='--scm', nargs='?',
                 help='Source control management. Currently supported: %s. Default: git' % ', '.join(
                     [s.name for s in scms.values()])),
            dict(name='--depth', nargs='?',
                 help='Number of revisions to fetch the repository when creating new program. Default: all revisions.'),
            dict(name='--protocol', nargs='?',
                 help='Transport protocol when fetching the repository when creating new program. ' +
                      'Supported: https, http, ssh, git. Default: inferred from URL.'),
            help='Clone a repository into a new directory',
            description=(
                    "Clone a repository with many new feature.\n"
                    "\"giti down\" is equal to \"git clone\" in function, with many new feature.\n"
                    "When using down, the auto proxy is default open.\n"
                    "Supported source control management: git"))
def down(url, proxy=False, scm='git', depth=None, protocol=None):
    if proxy:
        info("Proxy option is enable.", 0)
        addr = conf.get_proxy()
        info("Proxy address setting is " + addr)
        if not addr:
            warning("Proxy settings are not found. Using default proxy setting.")
            addr = '127.0.0.1:8087'

        os.system("git config --global http.proxy http://" + addr)
        os.system("git config --global https.proxy http://" + addr)
        os.system("git config --global http.sslverify false")

    os.system("git clone " + url)

    os.system("git config --global --unset http.proxy")
    os.system("git config --global --unset https.proxy")
    os.system("git config --global http.sslverify true")


@subcommand('set',
            dict(name='name', help='giti option name'),
            dict(name='value', help='giti option value'),
            help='Setup giti',
            description=(
                    "Set or modify parameters of giti.\n"
                    '"giti set" will change the profile in ~/.giticonf\n'
                    "You can change the profile manually as well."))
def set_(name, value):
    if name == 'proxy.address':
        conf.set_proxy(value)
        info("Proxy address setting is set to " + value)


def help_():
    return parser.print_help()


def main():
    global verbose, very_verbose, remainder, cwd_root, conf

    # Help messages adapt based on current dir
    cwd_root = os.getcwd()

    # Parse/run command
    if len(sys.argv) <= 1:
        help_()
        sys.exit(1)

    if '--version' in sys.argv:
        log(ver + "\n")
        sys.exit(0)

    conf = config.Config()
    pargs, remainder = parser.parse_known_args()
    status = 1

    try:
        very_verbose = pargs.very_verbose
        verbose = very_verbose or pargs.verbose
        info('Working path \"%s\"' % (os.getcwd()))
        status = pargs.command(pargs)
    except ProcessException as e:
        error(
            "\"%s\" returned error code %d.\n"
            "Command \"%s\" in \"%s\"" % (e[1], e[0], e[2], e[3]), e[0])
    except OSError as e:
        if e[0] == errno.ENOENT:
            error(
                "Could not detect one of the command-line tools.\n"
                "You could retry the last command with \"-v\" flag for verbose output\n", e[0])
        else:
            error('OS Error: %s' % e[1], e[0])
    except KeyboardInterrupt as e:
        info('User aborted!', -1)
        sys.exit(255)
    except Exception as e:
        if very_verbose:
            traceback.print_exc(file=sys.stdout)
        error("Unknown Error: %s" % e, 255)
    sys.exit(status or 0)


if __name__ == "__main__":
    main()
