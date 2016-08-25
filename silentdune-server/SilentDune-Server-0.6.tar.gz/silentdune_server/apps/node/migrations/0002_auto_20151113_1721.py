# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('node', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='node',
            name='machine_id',
            field=models.CharField(verbose_name='Node Machine ID', unique=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='node',
            name='system',
            field=models.CharField(verbose_name='Node System', unique=True, max_length=50),
        ),
    ]
