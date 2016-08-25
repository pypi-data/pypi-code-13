# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('proj', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WebLogView',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('user', models.IntegerField(default=-1, verbose_name='User ID')),
                ('wl_timestamp', models.DateTimeField(default=datetime.datetime.now, verbose_name='Timestamp')),
                ('wl_ipaddr', models.CharField(max_length=45, verbose_name='IP Address')),
                ('wl_content', models.CharField(max_length=1000, verbose_name='Description')),
                ('wl_action_flag', models.CharField(max_length=1, verbose_name='Action Flag')),
                ('wlt_code', models.CharField(max_length=10)),
                ('wlt_desc', models.CharField(max_length=250)),
                ('wlt_container', models.CharField(max_length=250)),
                ('wlt_retain_days', models.IntegerField(default=365)),
            ],
            options={
                'managed': False,
                'db_table': 'web_log_v',
            },
        ),
        migrations.CreateModel(
            name='WebLog',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('user', models.IntegerField(default=-1, verbose_name='User ID')),
                ('wl_timestamp', models.DateTimeField(default=datetime.datetime.now, verbose_name='Timestamp')),
                ('wl_ipaddr', models.CharField(max_length=45, verbose_name='IP Address')),
                ('wl_content', models.CharField(max_length=1000, verbose_name='Description')),
                ('wl_action_flag', models.CharField(max_length=1, verbose_name='Action Flag')),
            ],
            options={
                'db_table': 'web_log',
            },
        ),
        migrations.CreateModel(
            name='WebLogTypes',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('wlt_code', models.CharField(max_length=20, unique=True)),
                ('wlt_desc', models.CharField(max_length=250, verbose_name='Description')),
                ('wlt_container', models.CharField(max_length=250, verbose_name='Type Container')),
                ('wlt_retain_days', models.IntegerField(default=365, verbose_name='Retain Days')),
            ],
            options={
                'db_table': 'web_log_types',
            },
        ),
        migrations.AddField(
            model_name='weblog',
            name='wl_type',
            field=models.ForeignKey(to='proj.WebLogTypes', related_name='weblog'),
        ),
    ]
