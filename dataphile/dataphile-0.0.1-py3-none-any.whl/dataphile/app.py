# -*- coding: utf-8 -*-
#
# This file is part of DataPhile.
#
# Copyright (C) 2016 Geoffrey Lentner <glentner@nd.edu>
#
# DataPhile is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# DataPhile is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Annulus, LLC
   Scientific Computing Software.
"""

import tkinter as tk
from collections import OrderedDict

from .logging import Logging


class DataPhile(tk.Tk, Logging):
    """Application class for DataPhile.
    """

    # menu name, help, function, options
    menu_dictionary = OrderedDict([
        ('DataPhile', OrderedDict([

            ('About', {}),
            ('Version', {}),
            ('Quit', {}),
        ])),
        ('File', OrderedDict([
            ('Open', {}),
            ('Open Recent', {}),
            ('Save', {}),
            ('Save As', {}),
            ('Exprt', {}),
            ('Import', {}),
        ])),
        ('Edit', OrderedDict([
            ('Undo', {}),
            ('Redo', {}),
            ('Cut', {}),
            ('Copy', {}),
            ('Paste', {}),
        ])),
        ('View', OrderedDict([
            ('Zoom In', {}),
            ('Zoom Out', {}),
        ])),
        ('Analysis', OrderedDict([
            ('Apply Filter', {}),
            ('Fit Parameterization', {})
        ])),
        ('Help', OrderedDict([
            ('Search', {}),
            ('Documentation', {})
        ]))
    ])
        # The primary application menu.
        # This contains launchers for the different components of DataPhile and preferences



    def __init__(self):
        """Initialize the UI for DataPhile."""

        # we just want to make additions
        super().__init__()

        self.initLogger(loglevel='debug')

        # configure the main window
        self.title("DataPhile")
        self.geometry('600x400')
        self.mainFrame = tk.Frame(self)


        # create the menu structure
        self.__build_main_menu()

    # Private Operations
    def __build_main_menu(self):
        """Build the menu structure for DataPhile."""

        # Configure the toplevel menu
        self.mainMenu = tk.Menu(self)
        self.config(menu=self.mainMenu)


        self.subMenu = dict()
        for label, menu in self.menu_dictionary.items():
            self.subMenu[label] = tk.Menu(self.mainMenu)
            self.mainMenu.add_cascade(label=label, menu=self.subMenu[label])
            for sublabel, submenu in self.menu_dictionary[label].items():
                self.subMenu[label].add_command(label=sublabel, command=self.not_implemented)

    def not_implemented(self):
        self.log.warning('This feature is not yet implemented!')

    # Public API
    def start(self):
        """Run the main loop."""
        self.mainloop()
