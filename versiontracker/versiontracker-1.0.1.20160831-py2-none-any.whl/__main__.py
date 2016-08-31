#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
Given one or more software names, prints the following data about each software
piece:

* Latest stable version.
* Release date of the latest stable version.
* URL that is proof of the previous data.

Usage
=====

To get information about the latest stable version of one or more pieces of
software:

    versiontracker [app1 app2 …]

To get a list of supported pieces of software:

    versiontracker --list

To see this help:

    versiontracker --help


Example
=======

    $ versiontracker 0ad supertuxkart
    0ad: 0.0.17 (2014-10-12) @ https://sourceforge.net/projects/zero-ad/files/releases/
    supertuxkart: 0.8.1 (2013-11-25) @ https://sourceforge.net/projects/supertuxkart/files/SuperTuxKart/0.8.1/


Options
=======

-a, --all
        Shows the latest version of all supported pieces of software.

-l, --list
        Lists all supported pieces of software.

-h, --help
        Shows this command-line help. Any other option is ignored.

"""

from getopt import getopt, GetoptError
import sys

from termcolor import colored

from versiontracker import iter_latest_stable_versions, supported_software


def main():

    try:
        options, arguments = getopt(sys.argv[1:],
                                    "ahl", ["all", "help", "list"])
    except GetoptError as error:
        print(error)
        sys.exit(2)

    software = arguments
    list_command = False
    all_command = False

    for option, value in options:
        if option in ("-l", "--list"):
            list_command = True
        elif option in ("-a", "--all"):
            all_command = True
        elif option in ("-h", "--help"):
            print(__doc__)
            sys.exit()
        else:
            assert False, "unhandled option"

    if list_command:
        for software_piece in sorted(supported_software()):
            print(software_piece)
        sys.exit()
        
    if all_command:
        software = supported_software()

    if not software:
        print(u"Error: You must specify one or more names of pieces of "
              u"software as arguments, or use --all to work on all "
              u"supported software.\n")
        print(__doc__)
        sys.exit()

    for data in iter_latest_stable_versions(software):
        if "release_date" in data and data["release_date"]:
            print(u"{}: {} ({}) @ {}".format(
                colored(data["id"], attrs=["bold"]),
                colored(data["version"], "green"),
                colored(data["release_date"].strftime(
                    u"%Y-%m-%d"), "cyan"),
                colored(data["reference_url"], "magenta")))
        else:
            print(u"{}: {} @ {}".format(
                colored(data["id"], attrs=["bold"]),
                colored(data["version"], "green"),
                colored(data["reference_url"], "magenta")))
