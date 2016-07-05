# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-03 15:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consent', '0003_auto_20160628_1301'),
    ]

    operations = [
        migrations.AddField(
            model_name='dummypatientsourceinfo',
            name='pt_discharge_date',
            field=models.DateField(blank=True, null=True, verbose_name='Patient date of discharge'),  # noqa
        ),
        migrations.AddField(
            model_name='patientlookup',
            name='pt_discharge_date',
            field=models.DateField(blank=True, null=True, verbose_name='Patient date of discharge'),  # noqa
        ),
    ]
