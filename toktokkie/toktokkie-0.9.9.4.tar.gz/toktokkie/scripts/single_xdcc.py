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
import sys
import argparse
from typing import Tuple
from puffotter.fileops import ensure_directory_exists
from toktokkie.modules.objects.ProgressStruct import ProgressStruct
from toktokkie.modules.utils.downloaders.implementations.IrcLibImplementation import IrcLibImplementation


def parse_arguments() -> Tuple[str, str, str, str]:
    """
    Parses the command line parameters and establishes the important information from the input
    :return: the bot name, the pack number, the file destination, the irc server
    """
    parser = argparse.ArgumentParser(description="Downloads an XDCC pack")
    parser.add_argument("packstring", help="The XDCC get packstring, of form: '\"/msg BOTNAME xdcc send #PACKNUMBER\"'")
    parser.add_argument("--dest", help="Optional file path to store the downloaded file in")
    parser.add_argument("--server", help="Optional irc server. If this is not set, the script will automatically"
                                         "go through the most popular IRC servers")
    args = parser.parse_args()
    bot = args.packstring.split(" ")[1]
    pack = args.packstring.split(" ")[4].split("#")[1]
    return bot, pack, args.dest, args.server


def download_pack(xdcc_bot: str, xdcc_pack: int, target_destination: str, irc_server: str) -> None:
    """
    Downloads a single XDCC pack
    :param xdcc_bot: the bot from which the pack will be downloaded from
    :param xdcc_pack: the xdcc pack to download
    :param target_destination: the target file destination
    :param irc_server: the irc server to use
    :return: None
    """
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
                                      file_name_override=filename_override)
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
    bot, pack, dest, server = parse_arguments()
    download_pack(bot, int(pack), dest, server)

if __name__ == '__main__':
    main()
