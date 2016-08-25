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
        ('sql_data', '0003_basic_chainset'),
    ]

    # Maximum mariadb query packet size is 1MB, break into multiple commands if needed.
    # Use: "DO 0;" for reverse query on extra commands.

    # !!! Do not reorder records, the primary key value needs to always be the same for each record.
    #     Always add new records at the bottom of the list.
    operations = [
        migrations.RunSQL("""

            INSERT IGNORE INTO iptables_machine_subset (`id`, `name`, `platform`, `descr`, `notes`, `slot`, `sort_id`, `created`, `modified`)
                VALUES (2, 'Output Chain Logging', 'iptables', 'Log unmatched packets in Output chain.', '', 9800, 980, now(), now());
            INSERT IGNORE INTO iptables_chain (`id`, `name`, `machine_subset_id`, `created`, `modified`)
                VALUES (2, 'filter', 2, now(), now());

            # ipv4 - input
            INSERT IGNORE INTO iptables_ring (`id`, `name`, `version`, `chain_id`, `created`, `modified`)
                VALUES (5, 'output', 'ipv4', 2, now(), now());

            #INSERT IGNORE INTO iptables_rule (`id`, `enabled`, `sortid`, `descr`, `ring_id`, `created`, `modified`)
                #VALUES (13, 1, 1, 'Log unmatched packets', 5, now(), now());
                
            INSERT IGNORE INTO iptables_rule (`id`, `enabled`, `sort_id`, `descr`, `ring_id`, `created`, `modified`)
                VALUES (13, 1, 1, 'Log unmatched packets', 5, now(), now());                
            INSERT IGNORE INTO iptables_match (`id`, `name`, `rule_id`, `created`, `modified`)
                VALUES (11, 'limit', 13, now(), now());
            INSERT IGNORE INTO iptables_match_options (`option`, `value`, `invert`, `match_name_id`, `sort_id`, `created`, `modified`)
                VALUES ('--limit', '2/min', 0, 11, 1, now(), now());
            ##INSERT IGNORE INTO iptables_jump (`id`, `target`, `rule_id`, `created`, `modified`)
                ##VALUES (11, 'LOG', 13, now(), now());
            ##INSERT IGNORE INTO iptables_jump_options (`name`, `value`, `jump_id`, `created`, `modified`)
                ##VALUES ('--log-prefix', '"SDC Output:"', 11, now(), now());
            ##INSERT IGNORE INTO iptables_jump_options (`name`, `value`, `jump_id`, `created`, `modified`)
                ##VALUES ('--log-level', '4', 11, now(), now());

        """, """
        """),
    ]
