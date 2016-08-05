u"""
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

# Imports
from __future__ import absolute_import
from typing import List
from toktokkie.modules.objects.ProgressStruct import ProgressStruct
from toktokkie.modules.objects.XDCCPack import XDCCPack
from toktokkie.modules.utils.downloaders.implementations.IrcLibImplementation import IrcLibImplementation
from toktokkie.modules.utils.onlinedatagetters.TVDBGetter import TVDBGetter


class IrcLibDownloader(object):
    u"""
    XDCC Downloader that makes use of irclib to connect to IRC servers and request XDCC file
    transfers

    This Downloader requires only the irclib library, which means this is the most native downloader
    implemented in media-manager
    """

    packs = []
    u"""
    A list of the packs to download
    """

    progress_struct = None
    u"""
    A progress structure used to communicate with other threads, for example with a GUI to
    exchange information about the download progress
    """

    target_directory = u""
    u"""
    The target directory for the downloaded files
    """

    show_name = u""
    u"""
    The show name (only use when auto-renaming)
    """

    episode_number = -1
    u"""
    The first episode number (only use when auto-renaming)
    """

    season_number = -1
    u"""
    The season number (only use when auto-renaming)
    """

    auto_rename = False
    u"""
    This boolean is True if the program is supposed to automatically rename the downloaded files,
    but otherwise it defaults to False
    """

    # noinspection PyTypeChecker
    def __init__(self, packs, progress_struct, target_directory,
                 show_name = u"", episode_number = 0, season_number = 0):
        u"""
        Constructor for the IrcLibDownloader. It calls the constructor for the
        GenericDownloader class

        :param packs: the packs to be downloaded
        :param progress_struct: Structure that keeps track of download progress
        :param target_directory: The target download directory
        :param show_name: the show name for auto renaming
        :param episode_number: the (starting) episode number for auto renaming
        :param season_number: the season number for auto renaming
        :return: None
        """
        # Store variables
        self.packs = packs
        self.progress_struct = progress_struct
        self.target_directory = target_directory

        # Establish if the downloader should auto rename the files
        # Only auto rename if show name, season and episode are specified
        if show_name and episode_number > 0 and season_number > 0:
            self.show_name = show_name
            self.episode_number = episode_number
            self.season_number = season_number
            self.auto_rename = True

    def download_single(self, pack):
        u"""
        Downloads a single pack with the help of the irclib library
        and also auto-renames the resulting file if auto-rename is enabled

        :param pack: the pack to download
        :return: The file path to the downloaded file
        """
        # Print informational string, which file is being downloaded
        print u"Downloading pack: " + pack.to_string()

        if self.auto_rename:
            # Get the auto-renamed file name
            file_name = TVDBGetter(self.show_name, self.season_number, self.episode_number).get_formatted_episode_name()
            self.episode_number += 1
        else:
            file_name = None

        downloader = IrcLibImplementation(pack.server,
                                          pack.bot,
                                          pack.packnumber,
                                          self.target_directory,
                                          self.progress_struct,
                                          file_name_override=file_name)
        return downloader.start()

    # noinspection PyTypeChecker
    def download_loop(self):
        u"""
        Downloads all files stored by the Constructor and return a list of file paths to the
        downloaded files

        :return: the list of file paths of the downloaded files
        """
        files = []  # The downloaded file paths
        self.packs.sort(key=lambda x: x.filename)  # Sorts the packs by file name

        for pack in self.packs:  # Download each pack
            files.append(self.download_single(pack))  # Download pack and append file path to files list

            # Reset the progress of the single file to 0
            self.progress_struct.single_progress = 0
            self.progress_struct.single_size = 0

            self.progress_struct.total_progress += 1  # Increment progress structure
        return files
