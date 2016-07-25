# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('integration', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='webhook',
            name='date_created',
            field=models.DateTimeField(null=True, db_column=b'webhook_date_created', blank=True),
        ),
    ]
