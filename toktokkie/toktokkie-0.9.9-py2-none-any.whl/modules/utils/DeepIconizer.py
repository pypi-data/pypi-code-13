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
import platform
from typing import List
from tok_tokkie.modules.utils.iconizers.NautilusNemoIconizer import NautilusNemoIconizer
from tok_tokkie.modules.utils.iconizers.WindowsIconizer import WindowsIconizer


class DeepIconizer(object):
    u"""
    Class that handles the iconization of a directories using various kinds of iconizer methods
    """

    concrete_iconizer = None
    u"""
    The iconizer to be used when iconizing directories
    """

    def __init__(self, method):
        u"""
        Constructor for the DeepIconizer class. It takes an iconizer method as argument, which gets checked for
        validity.

        :param method: the method of iconization to be used
        :return: None
        """
        # Nautilus and Nemo use the same Iconizer technique
        if method == u"Nautilus" or method == u"Nemo":
            self.concrete_iconizer = NautilusNemoIconizer
        elif method == u"Windows":
            self.concrete_iconizer = WindowsIconizer
        else:
            # This should not happen in theory
            raise AssertionError(u"Invalid iconizing method passed as argument")

    def iconize(self, directory):
        u"""
        Iconizes a directory recursively. It browses through the directories content and triggers the
        __iconize_directory method once a '.icons' directory was found

        :param directory: The directory to be recursively browsed through in search of iconizable structures
        :return: None
        """
        # Iterate through every child
        for child in os.listdir(directory):

            # get the child's directory and folder icon paths
            child_path = os.path.join(directory, child)
            child_icon_path = os.path.join(child_path, u".icons")

            if os.path.isdir(child_path):  # only continue parsing if the child is a directory
                if os.path.isdir(child_icon_path):
                    # Found a .icons directory, start iconizing
                    self.__iconize_directory(child_path)
                else:
                    # Found no .icons directory, recursively search again through the child's subdirectories
                    self.iconize(child_path)

    def __iconize_directory(self, directory):
        u"""
        Starts the iconization process for a directory containing a .icons subdirectory

        :param directory: the directory to be iconized
        :return: None
        """
        # Get the folder icon directory
        folder_icon_directory = os.path.join(directory, u".icons")

        # Iconize the main directory
        self.concrete_iconizer.iconize(directory, os.path.join(folder_icon_directory, u"main"))

        # Iconize all subdirectories
        self.__iconize_children(directory, folder_icon_directory)

    def __iconize_children(self, directory, folder_icon_directory):
        u"""
        Recursively iconizes all subdirectories of a directory containing a .icons directory

        :param directory: The directory to be recursively searched for subdirectories to iconize
        :param folder_icon_directory:  The path to the folder icon directory
        :return:
        """
        # Check if we have permission to list the directory content
        try:
            children = os.listdir(directory)
        except PermissionError:
            # If not, skip this directory
            return

        # Iterate over all subdirectories
        for child in children:
            child_path = os.path.join(directory, child)  # The file system path to the child directory

            # If the child is either the .icons directory or not a directory at all, skip it
            if not os.path.isdir(child_path) or child == u".icons":
                continue

            # Otherwise, iconize the child
            else:
                self.concrete_iconizer.iconize(child_path, os.path.join(folder_icon_directory, child))

            # Repeat for all children of the child as well
            self.__iconize_children(child_path, folder_icon_directory)

    # noinspection PyTypeChecker
    @staticmethod
    def get_iconizer_options():
        u"""
        Returns a list of possible iconizer methods for the current platform the user is on

        :return: list of Iconizer options
        """
        # Linux Iconizers
        if platform.system() == u"Linux":
            return [u"Nautilus", u"Nemo"]

        # Windows Iconizers
        elif platform.system() == u"Windows":
            return [u"Windows"]

        # There are no other iconizers at the moment
        else:
            return []
