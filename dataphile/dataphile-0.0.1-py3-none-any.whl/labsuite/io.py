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

"""IO Methods for LabSuite Applications"""

def iec_to_csv(app, iec_file_path, csv_file_path=None):
    """Convert an 'iec' data file to CSV format.
    """

    app.log.info('Reading data from {file}'.format(file=iec_file_path))
    with open(iec_file_path, mode='r', buffering=None) as iec_file:
        iec_file_data = [line.strip() for line in iec_file.readlines()]

    iec_leader_code, iec_title, *_ = iec_file_data[0].split()
    iec_date = iec_file_data[2][len(leader_code):]

    if len(set([line[:len(iec_leader_code)] for line in iec_file_data])) != 1:
        app.log.error('{} does not meet expected IEC formatting'.format(iec_file_path))
    else:
        # strip the leader from the left-hand side of the data
        iec_file_data = [line.strip(iec_leader_code).strip() for line in iec_file_data]


    app.log.debug('{}: leader={}, name={}, data={}'
                  .format(os.path.basename(iec_file_path), iec_leader_code, iec_title, iec_date))
