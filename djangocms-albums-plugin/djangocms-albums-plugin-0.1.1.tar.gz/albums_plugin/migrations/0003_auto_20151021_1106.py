# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('albums_plugin', '0002_auto_20151021_1104'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photoalbum',
            name='albumset',
        ),
        migrations.DeleteModel(
            name='AlbumSet',
        ),
    ]
