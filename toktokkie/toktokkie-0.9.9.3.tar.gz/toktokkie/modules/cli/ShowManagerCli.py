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
from puffotter.interactive_cli.PuffOtterCli import PuffOtterCli


class ShowManagerCli(PuffOtterCli):
    """
    CLI for the Show Manager plugin
    """

    def __init__(self, parent: PuffOtterCli) -> None:
        """
        Constructor
        :param parent: the parent cli
        :return: void
        """
        super().__init__(parent)

    def start(self, title=None):
        """
        Starts the plugin main loop
        :return: void
        """
        super().start("Show Manager Plugin")

    def mainloop(self):
        """
        The plugin main loop
        :return: void
        """
        self.ask_user("Not Implemented. Enter quit to return.")
