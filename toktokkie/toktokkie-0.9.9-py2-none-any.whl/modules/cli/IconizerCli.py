u"""
LICENSE:

Copyright 2015,2016 Hermann Krumrey

This file is part of media-manager.

    media-manager is a program that allows convenient managing of various
    local media collections, mostly focused on video.

    media-manager is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    media-manager is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with media-manager.  If not, see <http://www.gnu.org/licenses/>.

LICENSE
"""

# imports
from __future__ import absolute_import
import os

from tok_tokkie.modules.cli.GenericCli import GenericCli
from tok_tokkie.modules.utils.DeepIconizer import DeepIconizer


class IconizerCli(GenericCli):
    u"""
    CLI for the Iconizer plugin

    It offers an interactive mode as well as an argument-driven mode
    """

    def __init__(self, parent):
        u"""
        Constructor of the IconizerCli class

        It calls the Constructor of the GenericCli class wit the parent argument and stores the
        parameter 'selected_iconizer' as a local class variable.

        :param parent: the parent CLI instance, to which the program returns to once this CLI has finished
        :return: None
        """
        super(IconizerCli, self).__init__(parent)

    def start(self, title = None):
        u"""
        Starts the plugin's main loop, calling the mainloop() method indefinitely

        Before doing so, it prints "ICONIZER PLUGIN" to the console

        :param title: Used as a dummy parameter to preserve the method signature from the super class
        :return: None
        """
        super(IconizerCli, self).start(u"ICONIZER PLUGIN\n")

    def mainloop(self, directory = None, selected_iconizer = None):
        u"""
        Starts the iconizing process

        :param directory: Overrides the directory to iconize, skipping the manual entry of the directory by the user
        :param selected_iconizer: Overrides the selected iconizer, making it possible to define an iconizer method
                            without manually asking the user
        :return None
        """

        # Ask the user for a directory path if none was defined by the method arguments
        if directory is None:
            directory = self.ask_user(u"Enter the directory to iconize:\n")

        # Strip surrounding quotation marks
        if directory.startswith(u"'") and directory.endswith(u"'") \
                or directory.startswith(u"\"") and directory.endswith(u"\""):
            directory = directory[1:-1]

        # Then check if the directory is a valid directory and also exists
        if not os.path.isdir(directory):
            # If not, start a new loop
            print u"No valid directory entered"
            return

        # Ask the user for an iconizer method if none was defined by the method arguments
        if selected_iconizer is None:
            print u"Which iconizing method would you like to use?\n"

            # list all Iconizer Options
            i = 1  # The index starts at 1 for a better user experience
            iconizer_dict = {}  # And also map them to indices using a dictionary
            for option in DeepIconizer.get_iconizer_options():
                print unicode(i) + u":" + option  # print
                iconizer_dict[i] = option  # and store
                i += 1  # Increment index

            # Now ask the user for his/her preferred iconizer method
            # Keep asking until the user gives a valid answer
            iconizer_selected = False
            while not iconizer_selected:
                user_iconizer = self.ask_user()  # ask the user
                try:
                    selected_iconizer = iconizer_dict[int(user_iconizer)]  # Try the user input as key in the dictionary
                    iconizer_selected = True  # If successful, break out of the loop
                except (ValueError, KeyError):
                    # ValueError when the user enters something that can't be parsed as an integer,
                    # KeyError when the integer value is out of bound for the dictionary
                    # Let's the user know he f***ed up. (Input an incorrect value)
                    print u"Invalid selection. Please enter the index of the preferred iconizer method\n"

        # Iconizes the selected directory
        print u"Iconizing Start"
        DeepIconizer(selected_iconizer).iconize(directory)
        print u"Iconizing End"
