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
        ('sql_data', '0002_web_log_types'),
    ]

    # Maximum mariadb query packet size is 1MB, break into multiple commands if needed.
    # Use: "DO 0;" for reverse query on extra commands.

    # !!! Do not reorder records, the primary key value needs to always be the same for each record.
    #     Always add new records at the bottom of the list.
    operations = [
        migrations.RunSQL("""
            INSERT IGNORE INTO iptables_machine_subset (`id`, `name`, `platform`, `descr`, `notes`, `slot`, `sort_id`, `created`, `modified`)
                VALUES (1, 'Admin Access', 'iptables', 'Allow administrative access to server', '', 110, 1, now(), now());
            INSERT IGNORE INTO iptables_chain (`id`, `name`, `machine_subset_id`, `created`, `modified`)
                VALUES (1, 'filter', 1, now(), now());

            # ipv4 - input
            INSERT IGNORE INTO iptables_ring (`id`, `name`, `version`, `chain_id`, `created`, `modified`)
                VALUES (1, 'input', 'ipv4', 1, now(), now());

            # ipv4 - input - Rule 1
            INSERT IGNORE INTO iptables_rule (`id`, `enabled`, `sort_id`, `descr`, `ring_id`, `created`, `modified`)
                VALUES (1, 1, 1, 'Allow existing connections through', 1, now(), now());
            INSERT IGNORE INTO iptables_match (`id`, `name`, `rule_id`, `created`, `modified`)
                VALUES (1, 'state', 1, now(), now());
            INSERT IGNORE INTO iptables_match_options (`option`, `value`, `invert`, `match_name_id`, `sort_id`, `created`, `modified`)
                VALUES ('--state', 'RELATED,ESTABLISHED', 0, 1, 1, now(), now());
            INSERT IGNORE INTO iptables_jump (`id`, `target`, `rule_id`, `created`, `modified`)
                VALUES (1, 'ACCEPT', 1, now(), now());

            # ipv4 - input - Rule 2
            INSERT IGNORE INTO iptables_rule (`id`, `enabled`, `sort_id`, `descr`, `ring_id`, `created`, `modified`, `ip_protocol_name`, `ip_protocol_invert`)
                VALUES (2, 1, 2, 'Allow icmp traffic', 1, now(), now(), 'icmp', 0 );
            #INSERT IGNORE INTO iptables_protocol (`name`, `invert`, `rule_id`, `created`, `modified`)
                #VALUES ('icmp', 0, 2, now(), now());
            INSERT IGNORE INTO iptables_jump (`id`, `target`, `rule_id`, `created`, `modified`)
                VALUES (2, 'ACCEPT', 2, now(), now());

            # ipv4 - input - Rule 3
            INSERT IGNORE INTO iptables_rule (`id`, `enabled`, `sort_id`, `descr`, `ring_id`, `created`, `modified`, `ifacein_name`, `ifacein_invert`,
                                               `source_address`, `source_mask`, `source_invert`, `dest_address`, `dest_mask`, `dest_invert`)
                VALUES (3, 1, 3, 'Allow local loop back device', 1, now(), now(), 'lo', 0, '127.0.0.1', '8', 0, '127.0.0.1', '8', 0 );
            #INSERT IGNORE INTO iptables_ifacein (`name`, `invert`, `rule_id`, `created`, `modified`)
                #VALUES ('lo', 0, 3, now(), now());
            #INSERT IGNORE INTO iptables_source (`address`, `mask`, `invert`, rule_id, `created`, `modified`)
                #VALUES ('127.0.0.1', '8', 0, 3, now(), now());
            #INSERT IGNORE INTO iptables_destination (`address`, `mask`, `invert`, rule_id, `created`, `modified`)
                #VALUES ('127.0.0.1', '8', 0, 3, now(), now());
            INSERT IGNORE INTO iptables_jump (`id`, `target`, `rule_id`, `created`, `modified`)
                VALUES (3, 'ACCEPT', 3, now(), now());

            # ipv4 - input - Rule 4
            INSERT IGNORE INTO iptables_rule (`id`, `enabled`, `sort_id`, `descr`, `ring_id`, `created`, `modified`, `ip_protocol_name`, `ip_protocol_invert` )
                VALUES (4, 1, 4, 'Allow ssh access to all', 1, now(), now(), 'tcp', 0 );
            #INSERT IGNORE INTO iptables_protocol (`name`, `invert`, `rule_id`, `created`, `modified`)
                #VALUES ('tcp', 0, 4, now(), now());
            INSERT IGNORE INTO iptables_match (`id`, `name`, `rule_id`, `created`, `modified`)
                VALUES (2, 'state', 4, now(), now());
            INSERT IGNORE INTO iptables_match_options (`option`, `value`, `invert`, `match_name_id`, `sort_id`, `created`, `modified`)
                VALUES ('--state', 'NEW', 0, 2, 1, now(), now());
            INSERT IGNORE INTO iptables_match (`id`, `name`, `rule_id`, `created`, `modified`)
                VALUES (3, 'tcp', 4, now(), now());
            INSERT IGNORE INTO iptables_match_options (`option`, `value`, `invert`, `match_name_id`, `sort_id`, `created`, `modified`)
                VALUES ('--dport', '22', 0, 3, 1, now(), now());
            INSERT IGNORE INTO iptables_jump (`id`, `target`, `rule_id`, `created`, `modified`)
                VALUES (4, 'ACCEPT', 4, now(), now());

            # ipv6 - input
            INSERT IGNORE INTO iptables_ring (`id`, `name`, `version`, `chain_id`, `created`, `modified`)
                VALUES (2, 'input', 'ipv6', 1, now(), now());

            # ipv6 - input - Rule 1
            INSERT IGNORE INTO iptables_rule (`id`, `enabled`, `sort_id`, `descr`, `ring_id`, `created`, `modified` )
                VALUES (5, 1, 1, 'Allow existing connections through', 2, now(), now() );
            INSERT IGNORE INTO iptables_match (`id`, `name`, `rule_id`, `created`, `modified`)
                VALUES (4, 'state', 5, now(), now());
            INSERT IGNORE INTO iptables_match_options (`option`, `value`, `invert`, `match_name_id`, `sort_id`, `created`, `modified`)
                VALUES ('--state', 'RELATED,ESTABLISHED', 0, 4, 1, now(), now());
            INSERT IGNORE INTO iptables_jump (`id`, `target`, `rule_id`, `created`, `modified`)
                VALUES (5, 'ACCEPT', 5, now(), now());

            # ipv6 - input - Rule 2
            INSERT IGNORE INTO iptables_rule (`id`, `enabled`, `sort_id`, `descr`, `ring_id`, `created`, `modified`, `ip_protocol_name`, `ip_protocol_invert` )
                VALUES (6, 1, 2, 'Allow icmp traffic', 2, now(), now(), 'icmp', 0 );
            #INSERT IGNORE INTO iptables_protocol (`name`, `invert`, `rule_id`, `created`, `modified`)
                #VALUES ('icmp', 0, 6, now(), now());
            INSERT IGNORE INTO iptables_jump (`id`, `target`, `rule_id`, `created`, `modified`)
                VALUES (6, 'ACCEPT', 6, now(), now());

            # ipv6 - input - Rule 3
            INSERT IGNORE INTO iptables_rule (`id`, `enabled`, `sort_id`, `descr`, `ring_id`, `created`, `modified`, `ifacein_name`, `ifacein_invert`,
                                              `source_address`, `source_mask`, `source_invert`, `dest_address`,`dest_mask`,`dest_invert` )
                VALUES (7, 1, 3, 'Allow local loop back device', 2, now(), now(), 'lo', 0, '::1', '128', 0, '::1', '128', 0 );
            #INSERT IGNORE INTO iptables_ifacein (`name`, `invert`, `rule_id`, `created`, `modified`)
                #VALUES ('lo', 0, 7, now(), now());
            #INSERT IGNORE INTO iptables_source (`address`, `mask`, `invert`, rule_id, `created`, `modified`)
                #VALUES ('::1', '128', 0, 7, now(), now());
            #INSERT IGNORE INTO iptables_destination (`address`, `mask`, `invert`, rule_id, `created`, `modified`)
                #VALUES ('::1', '128', 0, 7, now(), now());
            INSERT IGNORE INTO iptables_jump (`id`, `target`, `rule_id`, `created`, `modified`)
                VALUES (7, 'ACCEPT', 7, now(), now());

            # ipv6 - input - Rule 4
            INSERT IGNORE INTO iptables_rule (`id`, `enabled`, `sort_id`, `descr`, `ring_id`, `created`, `modified`, `ip_protocol_name`, `ip_protocol_invert` )
                VALUES (8, 1, 4, 'Allow ssh access to all', 2, now(), now(), 'tcp', 0 );
            #~ INSERT IGNORE INTO iptables_protocol (`name`, `invert`, `rule_id`, `created`, `modified`)
                #~ VALUES ('tcp', 0, 8, now(), now());
            INSERT IGNORE INTO iptables_match (`id`, `name`, `rule_id`, `created`, `modified`)
                VALUES (5, 'state', 8, now(), now());
            INSERT IGNORE INTO iptables_match_options (`option`, `value`, `invert`, `match_name_id`, `sort_id`, `created`, `modified`)
                VALUES ('--state', 'NEW', 0, 5, 1, now(), now());
            INSERT IGNORE INTO iptables_match (`id`, `name`, `rule_id`, `created`, `modified`)
                VALUES (6, 'tcp', 8, now(), now());
            INSERT IGNORE INTO iptables_match_options (`option`, `value`, `invert`, `match_name_id`, `sort_id`, `created`, `modified`)
                VALUES ('--dport', '22', 0, 6, 1, now(), now());
            INSERT IGNORE INTO iptables_jump (`id`, `target`, `rule_id`, `created`, `modified`)
                VALUES (8, 'ACCEPT', 8, now(), now());

            # ipv6 - output
            INSERT IGNORE INTO iptables_ring (`id`, `name`, `version`, `chain_id`, `created`, `modified` )
                VALUES (3, 'output', 'ipv4', 1, now(), now());

            # ipv4 - input - Rule 4
            INSERT IGNORE INTO iptables_rule (`id`, `enabled`, `sort_id`, `descr`, `ring_id`, `created`, `modified`, `ip_protocol_name`, `ip_protocol_invert` )
                VALUES (9, 1, 4, 'Allow ssh access to all', 3, now(), now(), 'tcp', 0);
            #~ INSERT IGNORE INTO iptables_protocol (`name`, `invert`, `rule_id`, `created`, `modified`)
                #~ VALUES ('tcp', 0, 9, now(), now());
            INSERT IGNORE INTO iptables_match (`id`, `name`, `rule_id`, `created`, `modified`)
                VALUES (7, 'state', 9, now(), now());
            INSERT IGNORE INTO iptables_match_options (`option`, `value`, `invert`, `match_name_id`, `sort_id`, `created`, `modified`)
                VALUES ('--state', 'ESTABLISHED', 0, 7, 1, now(), now());
            INSERT IGNORE INTO iptables_match (`id`, `name`, `rule_id`, `created`, `modified`)
                VALUES (8, 'tcp', 9, now(), now());
            INSERT IGNORE INTO iptables_match_options (`option`, `value`, `invert`, `match_name_id`, `sort_id`, `created`, `modified`)
                VALUES ('--sport', '22', 0, 8, 1, now(), now());
            INSERT IGNORE INTO iptables_jump (`id`, `target`, `rule_id`, `created`, `modified`)
                VALUES (9, 'ACCEPT', 9, now(), now());

            # ipv6 - output
            INSERT IGNORE INTO iptables_ring (`id`, `name`, `version`, `chain_id`, `created`, `modified`)
                VALUES (4, 'output', 'ipv6', 1, now(), now());

            # ipv4 - input - Rule 4
            INSERT IGNORE INTO iptables_rule (`id`, `enabled`, `sort_id`, `descr`, `ring_id`, `created`, `modified`, `ip_protocol_name`, `ip_protocol_invert` )
                VALUES (10, 1, 4, 'Allow ssh access to all', 4, now(), now(), 'tcp', 0 );
            #~ INSERT IGNORE INTO iptables_protocol (`name`, `invert`, `rule_id`, `created`, `modified`)
                #~ VALUES ('tcp', 0, 10, now(), now());
            INSERT IGNORE INTO iptables_match (`id`, `name`, `rule_id`, `created`, `modified`)
                VALUES (9, 'state', 10, now(), now());
            INSERT IGNORE INTO iptables_match_options (`option`, `value`, `invert`, `match_name_id`, `sort_id`, `created`, `modified`)
                VALUES ('--state', 'ESTABLISHED', 0, 9, 1, now(), now());
            INSERT IGNORE INTO iptables_match (`id`, `name`, `rule_id`, `created`, `modified`)
                VALUES (10, 'tcp', 10, now(), now());
            INSERT IGNORE INTO iptables_match_options (`option`, `value`, `invert`, `match_name_id`, `sort_id`, `created`, `modified`)
                VALUES ('--sport', '22', 0, 10, 1, now(), now());
            INSERT IGNORE INTO iptables_jump (`id`, `target`, `rule_id`, `created`, `modified`)
                VALUES (10, 'ACCEPT', 10, now(), now());



        """, """
            SET FOREIGN_KEY_CHECKS=0;
            TRUNCATE TABLE iptables_machine_subset;
            TRUNCATE TABLE iptables_chain;
            TRUNCATE TABLE iptables_ring;
            TRUNCATE TABLE iptables_rule;
            #~ TRUNCATE TABLE iptables_ifacein;
            #~ TRUNCATE TABLE iptables_ifaceout;
            #~ TRUNCATE TABLE iptables_protocol;
            #~ TRUNCATE TABLE iptables_source;
            #~ TRUNCATE TABLE iptables_destination;
            #~ TRUNCATE TABLE iptables_fragment;
            TRUNCATE TABLE iptables_match;
            TRUNCATE TABLE iptables_match_options;
            TRUNCATE TABLE iptables_jump;
            TRUNCATE TABLE iptables_jump_options;
            SET FOREIGN_KEY_CHECKS=1;
        """),
    ]

    # ipv4 - input - Rule 5
    # INSERT IGNORE INTO iptables_rule (`id`, `enabled`, `sortid`, `descr`, `ring_id`, `created`, `modified`)
    #     VALUES (5, 1, 5, 'Reject everything else', 1, now(), now());
    # INSERT IGNORE INTO iptables_jump (`id`, `target`, `rule_id`, `created`, `modified`)
    #     VALUES (5, 'REJECT', 5, now(), now());
    # INSERT IGNORE INTO iptables_jump_options (`id`, `name`, `value`, `jump_id`, `created`, `modified`)
    #     VALUES (1, '--reject-with', 'icmp-host-prohibited', 5, now(), now());

    # ipv4 - forward
    # INSERT IGNORE INTO iptables_ring (`id`, `name`, `version`, `chain_id`, `created`, `modified`)
    #     VALUES (2, 'forward', 'ipv4', 1, now(), now());
    #
    # # ipv4 - forward - Rule 1
    # INSERT IGNORE INTO iptables_rule (`id`, `enabled`, `sortid`, `descr`, `ring_id`, `created`, `modified`)
    #     VALUES (6, 1, 1, 'Reject everything else', 2, now(), now());
    # INSERT IGNORE INTO iptables_jump (`id`, `target`, `rule_id`, `created`, `modified`)
    #     VALUES (6, 'REJECT', 6, now(), now());
    # INSERT IGNORE INTO iptables_jump_options (`id`, `name`, `value`, `jump_id`, `created`, `modified`)
    #     VALUES (2, '--reject-with', 'icmp-host-prohibited', 6, now(), now());

    # ipv6 - input - Rule 5
    # INSERT IGNORE INTO iptables_rule (`id`, `enabled`, `sortid`, `descr`, `ring_id`, `created`, `modified`)
    #     VALUES (11, 1, 5, 'Reject everything else', 3, now(), now());
    # INSERT IGNORE INTO iptables_jump (`id`, `target`, `rule_id`, `created`, `modified`)
    #     VALUES (11, 'REJECT', 11, now(), now());
    # INSERT IGNORE INTO iptables_jump_options (`id`, `name`, `value`, `jump_id`, `created`, `modified`)
    #     VALUES (3, '--reject-with', 'icmp6-adm-prohibited', 11, now(), now());


    # ipv6 - forward
    # INSERT IGNORE INTO iptables_ring (`id`, `name`, `version`, `chain_id`, `created`, `modified`)
    #     VALUES (4, 'forward', 'ipv6', 1, now(), now());

    # ipv4 - forward - Rule 1
    # INSERT IGNORE INTO iptables_rule (`id`, `enabled`, `sortid`, `descr`, `ring_id`, `created`, `modified`)
    #     VALUES (12, 1, 1, 'Reject everything else', 4, now(), now());
    # INSERT IGNORE INTO iptables_jump (`id`, `target`, `rule_id`, `created`, `modified`)
    #     VALUES (12, 'REJECT', 12, now(), now());
    # INSERT IGNORE INTO iptables_jump_options (`id`, `name`, `value`, `jump_id`, `created`, `modified`)
    #     VALUES (4, '--reject-with', 'icmp6-adm-prohibited', 12, now(), now());
