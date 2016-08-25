# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rules', '0002_auto_20151020_2109'),
        ('iptables', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='IPTablesBundleSet',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('bundle', models.ForeignKey(to='rules.Bundle', related_name='bundle')),
            ],
            options={
                'db_table': 'iptables_bundleset',
            },
        ),
        migrations.AlterField(
            model_name='iptableschainset',
            name='slot',
            field=models.SmallIntegerField(verbose_name='Chain Set Slot', choices=[(10, 'Administration'), (20, 'SD Server'), (30, 'Identity Servers'), (40, 'Update Servers'), (50, 'DNS Servers'), (60, 'NTP Servers'), (1000, 'User Defined')]),
        ),
        migrations.AddField(
            model_name='iptablesbundleset',
            name='chainset',
            field=models.ForeignKey(to='iptables.IPTablesChainSet', related_name='chainsets'),
        ),
    ]
