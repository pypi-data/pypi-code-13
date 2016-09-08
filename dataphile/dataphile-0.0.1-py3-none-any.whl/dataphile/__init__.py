# -*- coding: utf-8 -*-
#
# This file is part of DataPhile.
#
# Copyright (c) 2016 Geoffrey Lentner <glentner@nd.edu>
#
# DataPhile is free software; you can redistribute it and/or modify it under
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

"""Initialize the DataPhile Software."""

import platform
import sys
import tkinter

# Global name
__appname__ = 'DataPhile'
__version__ = '0.0.1'
__authors__ = 'Geoffrey Lentner <glentner@nd.edu>'
__license__ = 'GPLv3'

# Import DataPhile libs
# Note: others DataPhile libs will be imported optionally
from dataphile.app import DataPhile


# Check Python version
if sys.version_info < (3, 5):
    print('DataPhile requires at least Python 3.5 to run.')
    sys.exit(1)


def main():
    """Main entry point for DataPhile.

    Select the mode (cli or gui)
    Run it...
    """

    try:
        app = DataPhile()

        # Log DataPhile and PSutil version
        app.log.info('Start DataPhile {0}'.format(__version__))
        app.log.info('{0} {1} detected'.format(platform.python_implementation(),
                                              platform.python_version()))

        app.start()

    except KeyboardInterrupt:
        app.log.info("Stopping DataPhile with KeyboardInterrupt")
        return 0

    except SystemExit:
        app.log.info("Stopping DataPhile with SystemExit")
        return 0
