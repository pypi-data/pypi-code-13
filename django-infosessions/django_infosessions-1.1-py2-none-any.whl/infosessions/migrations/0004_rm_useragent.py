# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('infosessions', '0003_auto_20150923_1219'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAgent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.TextField()),
                ('md5_hash', models.CharField(unique=True, max_length=32, db_index=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='sessioninfo',
            name='user_agent',
        ),
    ]
