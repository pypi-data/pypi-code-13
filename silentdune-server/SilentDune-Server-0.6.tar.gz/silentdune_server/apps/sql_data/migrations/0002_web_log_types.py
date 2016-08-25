#
# Authors: Robert Abram <robert.abram@entpack.com>
#
# Copyright (C) 2015 EntPack
# see file 'LICENSE' for use and warranty information
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


class Migration(migrations.Migration):

    dependencies = [
        ('sql_data', '0001_initial'),
    ]

    # Maximum mariadb query packet size is 1MB, break into multiple commands if needed.
    # Use: "DO 0;" for reverse query on extra commands.

    # !!! Do not reorder records, the primary key value needs to always be the same for each record.
    #     Always add new records at the bottom of the list.
    operations = [
        migrations.RunSQL("""
            INSERT INTO web_log_types (`wlt_code`, `wlt_desc`, `wlt_container`, `wlt_retain_days`, `created`, `modified`)
                VALUES ('UNKNOWN', 'Unknown Log Event', 'system.error', 180, now(), now());
            INSERT INTO web_log_types (`wlt_code`, `wlt_desc`, `wlt_container`, `wlt_retain_days`, `created`, `modified`)
                VALUES ('LOGIN', 'User Logged In', 'accounts.user', 365, now(), now());
            INSERT INTO web_log_types (`wlt_code`, `wlt_desc`, `wlt_container`, `wlt_retain_days`, `created`, `modified`)
                VALUES ('LOGIN_FAIL', 'User Failed To Login', 'accounts.user', 60, now(), now());
            INSERT INTO web_log_types (`wlt_code`, `wlt_desc`, `wlt_container`, `wlt_retain_days`, `created`, `modified`)
                VALUES ('LOGOUT', 'User Logged Out', 'accounts.user', 365, now(), now());
            INSERT INTO web_log_types (`wlt_code`, `wlt_desc`, `wlt_container`, `wlt_retain_days`, `created`, `modified`)
                VALUES ('ACCT_CREATED', 'Account Created', 'accounts', -1, now(), now());
            INSERT INTO web_log_types (`wlt_code`, `wlt_desc`, `wlt_container`, `wlt_retain_days`, `created`, `modified`)
                VALUES ('ACCT_ACTIVATED', 'Account activated', 'accounts', -1, now(), now());
            INSERT INTO web_log_types (`wlt_code`, `wlt_desc`, `wlt_container`, `wlt_retain_days`, `created`, `modified`)
                VALUES ('CHNG_PASS', 'User Changed Password', 'accounts.user', 180, now(), now());
        """, """
            SET FOREIGN_KEY_CHECKS=0; TRUNCATE TABLE web_log_types; SET FOREIGN_KEY_CHECKS=1;
        """),
    ]
