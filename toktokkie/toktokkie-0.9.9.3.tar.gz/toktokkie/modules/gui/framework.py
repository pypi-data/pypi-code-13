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
from gfworks.templates.generic.GenericGridTemplate import GenericGridTemplate


class GlobalGuiFramework(object):
    """
    A class that stores the currently selected GUI framework to enable cross-platform use using
    gfworks across all windows
    """

    selected_grid_gui_framework = GenericGridTemplate
    """
    This stores the selected GUI framework, it is initialized as generic object to avoid Import
    errors. The variable will be correctly set at some point in the main module's main method as
    either Gtk3GridTemplate or TkGridTemplate.
    """