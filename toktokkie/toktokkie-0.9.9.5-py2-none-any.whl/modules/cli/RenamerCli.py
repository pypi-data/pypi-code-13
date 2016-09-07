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

# imports
from __future__ import absolute_import
import os
from typing import List, Dict
from toktokkie.modules.utils.Renamer import Renamer
from puffotter.interactive_cli.PuffOtterCli import PuffOtterCli


class RenamerCli(PuffOtterCli):
    u"""
    CLI for the Renamer plugin, that lets the user choose a directory to use the renamer on.
    The directory's content is evaluated and the proposed changes are then printed to the console,
    where the user can then either approve or cancel the renaming process.
    """

    def __init__(self, parent):
        u"""
        Constructor of the RenamerCli, which only calls the GenericCli's constructor
        with the CLI's parent as argument.

        :param parent: the parent cli of the RenamerCli
        :return: None
        """
        super(RenamerCli, self).__init__(parent)

    def start(self, title = None):
        u"""
        Starts the plugin main loop by indefinitely looping the mainloop() method using the
        start() method of the GenericCli class with the title 'RENAMER PLUGIN'

        :param title: Just a dummy argument to maintain the same method signature as the GenericCli class
        :return: None
        """
        super(RenamerCli, self).start(u"RENAMER PLUGIN\n")

    def mainloop(self, directory = None, noconfirm = None):
        u"""
        Starts the renaming process. It can be run in both an interactive and an argument-driven mode
        not requiring user interaction.

        :param directory: Can be set to override the directory and bypassing user input
        :param noconfirm: If this is True, the renaming skips the confirming part
        :return: None
        """
        # If interactive mode is running, ask the user for a directory path
        if directory is None:
            directory = self.ask_user(u"Enter the show/series directory path:\n")

        # Strip surrounding quotation marks
        if directory.startswith(u"'") and directory.endswith(u"'") \
                or directory.startswith(u"\"") and directory.endswith(u"\""):
            directory = directory[1:-1]

        # If the directory is not a valid directory, exit immediately
        if not os.path.isdir(directory):
            print u"Not a valid directory path"
            return

        # Now that the directory is known, try to rename the contents
        renamer = Renamer(directory)  # Create a new Renamer object

        if not noconfirm:  # We need a manual confirmation by the user
            confirmation = renamer.request_confirmation()  # Request a confirmation
            if self.confirmer(confirmation):  # ask the user for confirmation, if successful start renaming
                print u"Renaming..."  # Let the user know we started renaming
                renamer.confirm(confirmation)  # Confirm the renaming process with the Renamer object
                renamer.start_rename()  # Start renaming
                print u"Renaming successful."  # Let the user know we have successfully renamed the files
            else:
                print u"Renaming cancelled."  # Message shown when the user cancels the process
        else:
            renamer.start_rename(True)  # Rename without confirmation, potentially dangerous

    @staticmethod
    def confirmer(confirmation):
        u"""
        Asks the user for confirmation before continuing the renaming process

        This is done by listing all changes to be made and asking the user a simple
        (y/n) question

        :param confirmation: the confirmation
        :return: False if the user did not confirm the rename, True otherwise.
        """
        # iterate over the confirmation list
        for element in confirmation:
            print u"OLD: " + element[u"old"]  # This is the old name of the file
            print u"NEW: " + element[u"new"] + u"\n"  # This is the new name of the file

        # Ask for confirmation
        response = raw_input(u"Proceed with renaming? This can not be undone. (y/n)")

        # If the answer was a lower-case y, return True, False otherwise
        return response == u"y"
