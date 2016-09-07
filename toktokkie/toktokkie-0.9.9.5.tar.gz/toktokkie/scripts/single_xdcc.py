#!/usr/bin/python
"""
LICENSE:
Copyright 2015,2016 Hermann Krumrey

This file is part of toktokkie.

    toktokkie is a program that allows convenient managing of various
    local media collections, mostly focused on video.

    toktokkie is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    toktokkie is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with toktokkie.  If not, see <http://www.gnu.org/licenses/>.
LICENSE
"""

# imports
import os
import re
import sys
import argparse
from typing import Tuple, List
from puffotter.fileops import ensure_directory_exists
from toktokkie.metadata import sentry
from toktokkie.modules.objects.ProgressStruct import ProgressStruct
from toktokkie.modules.utils.downloaders.implementations.IrcLibImplementation import IrcLibImplementation


def parse_arguments() -> Tuple[str, List[int], str, str]:
    """
    Parses the command line parameters and establishes the important information from the input
    :return: the bot name, the pack numbers, the file destination, the irc server
    """
    parser = argparse.ArgumentParser(description="Downloads an XDCC pack")
    parser.add_argument("packstring", help="The XDCC get packstring of form:\n"
                                           "\"/msg <BOTNAME> xdcc send #<PACKNUMBER>\"\n"
                                           "OR, if you want to download a range of packs:\n"
                                           "\"/msg <BOTNAME> xdcc send #<PN_START>-<PN_END>\"\n"
                                           "\n"
                                           "The variables in <> should be replaced with the user's input")
    parser.add_argument("--dest", help="Optional file path to store the downloaded file in")
    parser.add_argument("--server", help="Optional irc server. If this is not set, the script will automatically"
                                         "go through the most popular IRC servers")
    args = parser.parse_args()

    if not re.search(r"/msg [^ ]+ xdcc send #[0-9]+(-[0-9]+)?", args.packstring):
        print("Packstring does not match standard XDCC request. Aborting.")
        exit(1)

    bot = args.packstring.split(" ")[1]
    packs = [args.packstring.split(" ")[4].split("#")[1]]

    if re.search(r"[0-9]+-[0-9+]", packs[0]):
        packs = packs[0].split("-")

    packnumbers = []

    for pack in range(int(packs[0]), 1 + int(packs[len(packs) - 1])):
        packnumbers.append(int(pack))

    return bot, packnumbers, args.dest, args.server


def download_packs(xdcc_bot: str, xdcc_packs: List[int], target_destination: str, irc_server: str) -> None:
    """
    Downloads XDCC Packs
    :param xdcc_bot: the bot from which the pack will be downloaded from
    :param xdcc_packs: the xdcc packs to download
    :param target_destination: the target file destination
    :param irc_server: the irc server to use
    :return: None
    """
    for xdcc_pack in xdcc_packs:
        irc_server = irc_server if irc_server is not None else "irc.rizon.net"

        filename_override = None
        if target_destination is not None:
            if os.path.isdir(target_destination):
                pass
            else:
                filename_override = os.path.basename(target_destination).rsplit(".")[0]
                target_destination = os.path.dirname(target_destination)
                ensure_directory_exists(target_destination)
        else:
            target_destination = os.getcwd()

        filename_override = None if not filename_override else filename_override  # Turn empty string into None object
        downloader = IrcLibImplementation(irc_server,
                                          xdcc_bot,
                                          xdcc_pack,
                                          target_destination,
                                          ProgressStruct(),
                                          file_name_override=filename_override,
                                          verbosity_level=10)
        downloader.start()


def check_target_directory(args_maxlength: int) -> Tuple[str, str]:
    """
    Checks the user's arguments for the target directory and file
    :param args_maxlength: the maximum length of the arguments
    :return: the directory, the filename
    """
    if len(sys.argv) == args_maxlength:
        path = sys.argv[args_maxlength - 1]
        if os.path.isdir(path):
            return path, ""
        else:
            directory = os.path.dirname(path)
            if not os.path.isdir:
                os.makedirs(directory)
            return directory, os.path.basename(path)
    else:
        return os.getcwd(), ""


def main() -> None:
    """
    Starts the script and downloads an XDCC pack on valid input
    Invalid input will display a usage message

    The script supports entering the XDCC message string in parentheses and without

    Usage: single-xdcc (")/msg botname xdcc send #pack(") destination
    :return: None
    """
    # noinspection PyBroadException
    try:
        bot, packs, dest, server = parse_arguments()
        download_packs(bot, packs, dest, server)
    except KeyboardInterrupt:
        print("\nThanks for using the Tok Tokkie media manager!")
        sys.exit(0)
    except:
        sentry.captureException()


if __name__ == '__main__':
    main()
