# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('rules', '0002_auto_20151020_2109'),
    ]

    operations = [
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('platform', models.CharField(verbose_name='Firewall Platform', max_length=30, choices=[('iptables', 'IPTables')])),
                ('system', models.CharField(verbose_name='Node System', max_length=50)),
                ('dist', models.CharField(verbose_name='Node Distribution', max_length=100)),
                ('dist_version', models.CharField(verbose_name='Node Distribution Version', max_length=50)),
                ('python_version', models.CharField(verbose_name='Node Distribution Version', max_length=255)),
                ('machine_id', models.CharField(verbose_name='Node Machine ID', max_length=100)),
                ('register_date', models.DateField(verbose_name='Registration Timestamp', default=datetime.date.today)),
                ('last_date', models.DateField(verbose_name='Last Connection Timestamp', default=datetime.date.today)),
                ('sync', models.BooleanField(verbose_name='Node Synchronized', default=True)),
                ('notes', models.CharField(verbose_name='Notes', max_length=4000, default='')),
            ],
            options={
                'db_table': 'node',
            },
        ),
        migrations.CreateModel(
            name='NodeBundle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bundle', models.ForeignKey(to='rules.Bundle')),
                ('node', models.ForeignKey(to='node.Node')),
            ],
            options={
                'db_table': 'node_bundle',
            },
        ),
    ]
