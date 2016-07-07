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
from gfworks.templates.generic.GenericGridTemplate import GenericGridTemplate


class GlobalGuiFramework(object):
    u"""
    A class that stores the currently selected GUI framework to enable cross-platform use using
    gfworks. Future plans of gfworks may be able to make this admittedly ugly construct
    obsolete, but as of right now it is required
    """

    selected_grid_gui_framework = GenericGridTemplate
    u"""
    This stores the selected GUI framework, it is initialized as generic object to avoid Import
    errors. The variable will be correctly set at some point in the main module's main method as
    either Gtk3GridTemplate or TkGridTemplate.
    """