# -*- coding: utf-8 -*-
#
# This file is part of LabSuite.
#
# Copyright (c) 2016 Geoffrey Lentner <glentner@nd.edu>
#
# LabSuite is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

"""Common logging technique used throughout 'project' package.
"""

import logging
import colorlog

formatter = colorlog.ColoredFormatter(
    "[%(log_color)s%(asctime)s %(name)s%(reset)s] %(message)s",
    datefmt=None,
    reset=True,
    log_colors={
        'DEBUG':    'cyan',
        'INFO':     'green',
        'WARNING':  'yellow',
        'ERROR':    'red',
        'CRITICAL': 'red,bg_white',
    },
    secondary_log_colors={},
    style='%')

console = colorlog.StreamHandler()
console.setFormatter(formatter)


class Logging:
    """Mixin class which implements custom logging messages.
    """

    def initLogger(self, loglevel='info'):
        """Create the logging object.

        example:
            def __init__(self, ...):
                ...
                self.initLogger(loglevel='debug')
        """
        self.log = colorlog.getLogger(self.__class__.__name__)
        self.log.addHandler(console)
        self.log.setLevel(getattr(logging, str(loglevel).upper()))
