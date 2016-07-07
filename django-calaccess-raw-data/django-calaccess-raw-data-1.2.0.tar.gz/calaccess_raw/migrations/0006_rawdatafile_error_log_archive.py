# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-06 17:19
from __future__ import unicode_literals

import calaccess_raw
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calaccess_raw', '0005_auto_20160705_2145'),
    ]

    operations = [
        migrations.AddField(
            model_name='rawdatafile',
            name='error_log_archive',
            field=models.FileField(blank=True, help_text='An archive of the error log containing .TSV file lines that could not be cleaned and are excluded from the .CSV file.', max_length=255, upload_to=calaccess_raw.archive_directory_path, verbose_name='archive of error log'),
        ),
    ]
