# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('integration', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='integration',
            name='all_products',
            field=models.BooleanField(default=True, db_column=b'integration_all_products'),
        ),
    ]
