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

"""Initialize the LabSuite Software."""

import platform
import sys
import tkinter

# Global name
__appname__ = 'LabSuite'
__version__ = '0.0.1'
__authors__ = 'Geoffrey Lentner <glentner@nd.edu>'
__license__ = 'GPLv3'

# Import LabSuite libs
# Note: others LabSuite libs will be imported optionally
from labsuite.app import LabSuite


# Check Python version
if sys.version_info < (3, 5):
    print('LabSuite requires at least Python 3.5 to run.')
    sys.exit(1)


def main():
    """Main entry point for LabSuite.

    Select the mode (cli or gui)
    Run it...
    """

    try:
        app = LabSuite()

        # Log LabSuite and PSutil version
        app.log.info('Start LabSuite {0}'.format(__version__))
        app.log.info('{0} {1} detected'.format(platform.python_implementation(),
                                              platform.python_version()))

        app.start()

    except KeyboardInterrupt:
        app.log.info("Stopping LabSuite with KeyboardInterrupt")
        return 0

    except SystemExit:
        app.log.info("Stopping LabSuite with SystemExit")
        return 0
