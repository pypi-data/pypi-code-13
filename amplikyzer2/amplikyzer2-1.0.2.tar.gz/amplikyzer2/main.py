# amplikyzer2.main
# (c) Sven Rahmann 2011--2012
"""
Parse the command line arguments and execute the appropriate submodule.
"""

import argparse
from collections import OrderedDict
from random import seed
import logging
from time import time

from .analysis import analyze_sff, analyze_fastq
from . import statistics
from . import align
from . import methylation
from . import printreads
from .core import EXT_CONFIG


###################################################################################################
# main; interface for geniegui

def get_argument_parser():
    """Return an ArgumentParser object p with this module's options;
    with an additional dict attribute p._geniegui to specify
    "special" treatment (file/path dialogs) for some options.
    """
    # define available subcommands as dict:
    # name = (sort_order, helpstring, module)
    # each module must have a buildparser function and a main function.
    _subcommands = dict(
        printreads=(
            0, "print reads of an .sff file",
            printreads),
        analyzesff=(
            1, "analyze .sff files (identify key, mid, tag, primer, ROI for each read)",
            analyze_sff),
        analyzefastq=(
            2, "analyze .fastq files (identify key, mid, tag, primer, ROI for each read)",
            analyze_fastq),
        statistics=(
            3, "show statistics for an analyzed dataset",
            statistics),
        align=(
            4, "output a multiple alignment of all reads of a locus for a given MID",
            align),
        methylation=(
            5, "do a methylation analysis of a given locus and MID",
            methylation),
        )
    # obtain the ArgumentParser object 'p'
    p = argparse.ArgumentParser(
        # formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="amplikyzer2: an amplicon analyzer",
        epilog="In development. Use at your own Risk!"
        )
    p._geniegui = dict()
    # global options for all subcommands
    p.add_argument(
        "--path", "-p", default="",
        help="project path (directory) containing an .sff file")
    p._geniegui["--path"] = "dir"
    p.add_argument(
        "--conf", nargs="+", default=["*"+EXT_CONFIG], metavar="FILE",
        help="names of configuration files with MIDS, TAGS, LOCI, LABELS")
    p.add_argument(
        '-', dest='__narg_delimiter', action="store_true",
        help=argparse.SUPPRESS)
    p.add_argument(
        "--rngseed", type=int, metavar="INT",
        help=argparse.SUPPRESS)
    # add subcommands to parser
    subs = p.add_subparsers()
    subs.required = True
    subs.dest = 'subcommand'
    subcommands = OrderedDict(sorted(_subcommands.items(), key=lambda x: x[1][0]))
    for (scname, (_, schelp, scmodule)) in subcommands.items():
        subcommandparser = subs.add_parser(
            # formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            scname, help=schelp, description=scmodule.__doc__)
        subcommandparser._geniegui = dict()
        subcommandparser.set_defaults(func=scmodule.main)
        scmodule.buildparser(subcommandparser)
    return p


class InfoTimeFormatter(logging.Formatter):
    def __init__(self, fmt=None, datefmt=None):
        super().__init__(fmt, datefmt, style="%")
        self.created = time()

    def format(self, record):
        levelname = ""
        if record.levelno != logging.INFO:
            return "{levelname}: {msg}".format(
                levelname=record.levelname, msg=super().format(record))
        return "@{time:.2f} {msg}".format(
            time=record.created - self.created, msg=super().format(record))


def main(args=None):
    """main function; interface for geniegui"""
    log_handler = logging.StreamHandler()
    log_handler.setFormatter(InfoTimeFormatter())
    logging.basicConfig(level=logging.INFO, handlers=[log_handler])

    p = get_argument_parser()
    pargs = p.parse_args() if args is None else p.parse_args(args)
    if pargs.rngseed is not None:
        seed(pargs.rngseed)
    pargs.func(pargs)  # call the appropriate subcommand function


def gui():
    import geniegui
    geniegui.main(["amplikyzer2"])


__NOTES = """
Description of CWF format and other formats:
http://454.com/my454/documentation/gs-flx-system/emanuals.asp
"""
