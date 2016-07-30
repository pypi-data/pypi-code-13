# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import albums_plugin.models


class Migration(migrations.Migration):

    dependencies = [
        ('albums_plugin', '0005_albumupload'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='thumb',
            field=models.ImageField(null=True, upload_to=albums_plugin.models.generate_folder_path, blank=True),
            preserve_default=True,
        ),
    ]
