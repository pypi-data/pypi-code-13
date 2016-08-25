#
# Authors: Robert Abram <robert.abram@entpack.com>
#
# Copyright (C) 2015 EntPack
# see file 'COPYING' for use and warranty information
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import migrations

# TODO: This file needs to be removed from the sql_data directory or deleted.
# Note: This data should only be loaded into the database during the initial install, and never again.
# Note: Only data that can safely be truncated or deleted during an update should be in this directory.


class Migration(migrations.Migration):

    dependencies = [
        ('sql_data', '0005_reject_chainset'),
    ]

    # Maximum mariadb query packet size is 1MB, break into multiple commands if needed.
    # Use: "DO 0;" for reverse query on extra commands.

    # !!! Do not reorder records, the primary key value needs to always be the same for each record.
    #     Always add new records at the bottom of the list.
    operations = [
        migrations.RunSQL("""

            INSERT IGNORE INTO rule_bundle (`id`, `name`, `platform`, `descr`, `notes`, `default`, `created`, `modified`)
                VALUES (1, 'Basic Admin', 'iptables', 'Basic administration access to servers', '', 1, now(), now());

            INSERT IGNORE INTO iptables_machine_set (`bundle_id`, `machine_subset_id`, `created`, `modified`)
                VALUES (1, 1, now(), now());
            INSERT IGNORE INTO iptables_machine_set (`bundle_id`, `machine_subset_id`, `created`, `modified`)
                VALUES (1, 2, now(), now());
            INSERT IGNORE INTO iptables_machine_set (`bundle_id`, `machine_subset_id`, `created`, `modified`)
                VALUES (1, 3, now(), now());
            INSERT IGNORE INTO iptables_machine_set (`bundle_id`, `machine_subset_id`, `created`, `modified`)
                VALUES (1, 4, now(), now());
            INSERT IGNORE INTO iptables_machine_set (`bundle_id`, `machine_subset_id`, `created`, `modified`)
                VALUES (1, 5, now(), now());


        """, """
            SET FOREIGN_KEY_CHECKS=0;
            TRUNCATE TABLE rule_bundle;
            TRUNCATE TABLE iptables_machine_set;
            SET FOREIGN_KEY_CHECKS=1;
        """),
    ]
