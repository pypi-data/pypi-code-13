#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# Primitivus: a SAT frontend
# Copyright (C) 2009-2016 Jérôme Poisson (goffi@goffi.org)

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from sat_frontends.quick_frontend import constants


class Const(constants.Const):

    APP_NAME = "jp"
    PLUGIN_CMD = "commands"
    PLUGIN_OUTPUT = "outputs"
    OUTPUT_TEXT = 'text' # blob of unicode text
    OUTPUT_DICT = 'dict'
    OUTPUT_LIST = 'list'
    OUTPUT_TYPES = (OUTPUT_TEXT, OUTPUT_DICT, OUTPUT_LIST)

    # exit codes
    EXIT_OK = 0
    EXIT_ERROR = 1 # generic error, when nothing else match
    EXIT_BAD_ARG = 2 # arguments given by user are bad
    EXIT_FILE_NOT_EXE = 126 # a file to be executed was found, but it was not an executable utility (cf. man 1 exit)
    EXIT_CMD_NOT_FOUND = 127 # a utility to be executed was not found (cf. man 1 exit)
    EXIT_SIGNAL_INT = 128 # a command was interrupted by a signal (cf. man 1 exit)
