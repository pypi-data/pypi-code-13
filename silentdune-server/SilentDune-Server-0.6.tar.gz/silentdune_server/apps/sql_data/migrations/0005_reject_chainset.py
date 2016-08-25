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
        ('sql_data', '0004_logging_chainset'),
    ]

    # Maximum mariadb query packet size is 1MB, break into multiple commands if needed.
    # Use: "DO 0;" for reverse query on extra commands.

    # !!! Do not reorder records, the primary key value needs to always be the same for each record.
    #     Always add new records at the bottom of the list.
    operations = [
        migrations.RunSQL("""

            INSERT IGNORE INTO iptables_machine_subset (`id`, `name`, `platform`, `descr`, `notes`, `slot`, `sort_id`, `created`, `modified`)
                VALUES (3, 'Reject Input Chain Packets', 'iptables', 'Reject unmatched packets in Input chain.', '', 9900, 9900, now(), now());
            INSERT IGNORE INTO iptables_chain (`id`, `name`, `machine_subset_id`, `created`, `modified`)
                VALUES (3, 'filter', 3, now(), now());

            # ipv4 - input
            INSERT IGNORE INTO iptables_ring (`id`, `name`, `version`, `chain_id`, `created`, `modified`)
                VALUES (6, 'input', 'ipv4', 3, now(), now());

            INSERT IGNORE INTO iptables_rule (`id`, `enabled`, `sort_id`, `descr`, `ring_id`, `created`, `modified`)
                VALUES (14, 1, 1, 'Reject ipv4 unmatched packets in input chain', 6, now(), now());
            INSERT IGNORE INTO iptables_jump (`id`, `target`, `rule_id`, `created`, `modified`)
                VALUES (12, 'REJECT', 14, now(), now());
            INSERT IGNORE INTO iptables_jump_options (`name`, `value`, `jump_id`, `created`, `modified`)
                VALUES ('--reject-with', 'icmp-host-prohibited', 12, now(), now());

            # ipv6 - input
            INSERT IGNORE INTO iptables_ring (`id`, `name`, `version`, `chain_id`, `created`, `modified`)
                VALUES (7, 'input', 'ipv6', 3, now(), now());

            INSERT IGNORE INTO iptables_rule (`id`, `enabled`, `sort_id`, `descr`, `ring_id`, `created`, `modified`)
                VALUES (15, 1, 1, 'Reject ipv6 unmatched packets in input chain', 7, now(), now());
            INSERT IGNORE INTO iptables_jump (`id`, `target`, `rule_id`, `created`, `modified`)
                VALUES (13, 'REJECT', 15, now(), now());
            INSERT IGNORE INTO iptables_jump_options (`name`, `value`, `jump_id`, `created`, `modified`)
                VALUES ('--reject-with', 'icmp6-adm-prohibited', 13, now(), now());

            # Reject Chainset - Forward chain
            INSERT IGNORE INTO iptables_machine_subset (`id`, `name`, `platform`, `descr`, `notes`, `slot`, `sort_id`, `created`, `modified`)
                VALUES (4, 'Reject Forward Chain Packets', 'iptables', 'Reject unmatched packets in Forward chain.', '', 9900, 9991, now(), now());
            INSERT IGNORE INTO iptables_chain (`id`, `name`, `machine_subset_id`, `created`, `modified`)
                VALUES (4, 'filter', 4, now(), now());

            # ipv4 - forward
            INSERT IGNORE INTO iptables_ring (`id`, `name`, `version`, `chain_id`, `created`, `modified`)
                VALUES (8, 'forward', 'ipv4', 4, now(), now());

            # ipv4 - forward
            INSERT IGNORE INTO iptables_rule (`id`, `enabled`, `sort_id`, `descr`, `ring_id`, `created`, `modified`)
                VALUES (16, 1, 1, 'Reject ipv4 unmatched packets in forward chain', 8, now(), now());
            INSERT IGNORE INTO iptables_jump (`id`, `target`, `rule_id`, `created`, `modified`)
                VALUES (14, 'REJECT', 16, now(), now());
            INSERT IGNORE INTO iptables_jump_options (`name`, `value`, `jump_id`, `created`, `modified`)
                VALUES ('--reject-with', 'icmp-host-prohibited', 14, now(), now());

            # ipv6 - forward
            INSERT IGNORE INTO iptables_ring (`id`, `name`, `version`, `chain_id`, `created`, `modified`)
                VALUES (9, 'forward', 'ipv6', 4, now(), now());

            # ipv6 - forward
            INSERT IGNORE INTO iptables_rule (`id`, `enabled`, `sort_id`, `descr`, `ring_id`, `created`, `modified`)
                VALUES (17, 1, 1, 'Reject ipv6 unmatched packets in forward chain', 9, now(), now());
            INSERT IGNORE INTO iptables_jump (`id`, `target`, `rule_id`, `created`, `modified`)
                VALUES (15, 'REJECT', 17, now(), now());
            INSERT IGNORE INTO iptables_jump_options (`name`, `value`, `jump_id`, `created`, `modified`)
                VALUES ('--reject-with', 'icmp6-adm-prohibited', 15, now(), now());

            # Reject Chainset - Output chain
            INSERT IGNORE INTO iptables_machine_subset (`id`, `name`, `platform`, `descr`, `notes`, `slot`, `sort_id`, `created`, `modified`)
                VALUES (5, 'Reject Output Chain Packets', 'iptables', 'Reject unmatched packets in Output chain.', '', 9900, 9992, now(), now());
            INSERT IGNORE INTO iptables_chain (`id`, `name`, `machine_subset_id`, `created`, `modified`)
                VALUES (5, 'filter', 5, now(), now());

            # ipv4 - output
            INSERT IGNORE INTO iptables_ring (`id`, `name`, `version`, `chain_id`, `created`, `modified`)
                VALUES (10, 'output', 'ipv4', 5, now(), now());

            # ipv4 - output
            INSERT IGNORE INTO iptables_rule (`id`, `enabled`, `sort_id`, `descr`, `ring_id`, `created`, `modified` )
                VALUES (18, 1, 1, 'Reject ipv4 unmatched packets in forward chain', 10, now(), now() );
            INSERT IGNORE INTO iptables_jump (`id`, `target`, `rule_id`, `created`, `modified`)
                VALUES (16, 'REJECT', 18, now(), now());
            INSERT IGNORE INTO iptables_jump_options (`name`, `value`, `jump_id`, `created`, `modified`)
                VALUES ('--reject-with', 'icmp-host-prohibited', 16, now(), now());

            # ipv6 - output
            INSERT IGNORE INTO iptables_ring (`id`, `name`, `version`, `chain_id`, `created`, `modified`)
                VALUES (11, 'output', 'ipv6', 5, now(), now());

            # ipv6 - output
            INSERT IGNORE INTO iptables_rule (`id`, `enabled`, `sort_id`, `descr`, `ring_id`, `created`, `modified`)
                VALUES (19, 1, 1, 'Reject ipv6 unmatched packets in forward chain', 11, now(), now());
            INSERT IGNORE INTO iptables_jump (`id`, `target`, `rule_id`, `created`, `modified`)
                VALUES (17, 'REJECT', 19, now(), now());
            INSERT IGNORE INTO iptables_jump_options (`name`, `value`, `jump_id`, `created`, `modified`)
                VALUES ('--reject-with', 'icmp6-adm-prohibited', 17, now(), now());

        """, """
        """),
    ]
