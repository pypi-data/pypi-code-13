# -*- coding: utf-8 -*-
#
# This file is part of LabSuite.
#
# Copyright (C) 2016 Geoffrey Lentner <glentner@nd.edu>
#
# LabSuite is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# LabSuite is distributed in the hope that it will be useful,
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
from .logging import Logging


class LabSuite(tk.Tk, Logging):
    """Application class for LabSuite.

    Attributes
    ----------

    Methods
    -------

    Raises
    ------

    See Also
    --------

    """

    def __init__(self):
        """Initialize the UI for LabSuite."""

        # we just want to make additions
        super().__init__()

        self.initLogger(loglevel='debug')

        # configure the main window
        self.title("LabSuite")
        self.geometry('600x400')
        self.mainFrame = tk.Frame(self)


        # create the menu structure
        self.__build_main_menu()

    # Private Operations
    def __build_main_menu(self):
        """Build the menu structure for LabSuite."""

        # Configure the toplevel menu
        self.mainMenu = tk.Menu(self)
        self.config(menu=self.mainMenu)

        # Add an application (i.e., "LabSuite") menu
        self.appMenu = tk.Menu(self.mainMenu)
        self.mainMenu.add_cascade(label="LabSuite", menu=self.appMenu)
        self.appMenu.add_command(label="About", command=self.not_implemented)
        self.appMenu.add_command(label="Version", command=self.not_implemented)
        self.appMenu.add_separator()
        self.appMenu.add_command(label="Preferences", command=self.not_implemented)
        self.appMenu.add_separator()
        self.appMenu.add_command(label="Quit LabSuite", command=self.not_implemented)

        # Add a "File" menu
        self.fileMenu = tk.Menu(self.mainMenu)
        self.mainMenu.add_cascade(label="File", menu=self.fileMenu)
        self.fileMenu.add_command(label="New Project",  command=self.not_implemented)
        self.fileMenu.add_command(label="Open", command=self.not_implemented)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Save", command=self.not_implemented)
        self.fileMenu.add_command(label="Save As", command=self.not_implemented)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Close", command=self.not_implemented)
        self.fileMenu.add_separator()

        # Add an "Edit" menu
        self.editMenu = tk.Menu(self.mainMenu)
        self.mainMenu.add_cascade(label="Edit", menu=self.editMenu)
        # self.editMenu.add_command(label="Preferences", command=self.not_implemented)

        # Add a "View" menu (for plots)
        self.viewMenu = tk.Menu(self.mainMenu)
        self.mainMenu.add_cascade(label="View", menu=self.viewMenu)
        self.viewMenu.add_command(label="Zoom", command=self.not_implemented)

        # Add an "Analysis" menu (for plots)
        self.analysisMenu = tk.Menu(self.mainMenu)
        self.mainMenu.add_cascade(label="Analysis", menu=self.analysisMenu)
        self.analysisMenu.add_command(label="Filters", command=self.not_implemented)
        self.analysisMenu.add_command(label="Fit Data", command=self.not_implemented)


    def not_implemented(self):
        self.log.warning('This feature is not yet implemented!')

    # Public API
    def start(self):
        """Run the main loop."""
        self.mainloop()
