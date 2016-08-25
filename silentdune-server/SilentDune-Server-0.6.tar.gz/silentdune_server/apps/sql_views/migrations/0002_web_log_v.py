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
        ('sql_views', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL("""
            CREATE OR REPLACE VIEW web_log_v AS
            SELECT web_log.*,
                web_log_types.wlt_code,
                web_log_types.wlt_desc,
                web_log_types.wlt_container,
                web_log_types.wlt_retain_days
              FROM web_log LEFT JOIN web_log_types ON
              web_log.id = web_log_types.id
        """, """
            DROP VIEW IF EXISTS web_log_v
        """),
    ]
