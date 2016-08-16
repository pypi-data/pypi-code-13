# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Datalogger',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('event_id', models.CharField(max_length=100, null=True, verbose_name='\u4e8b\u4ef6ID', blank=True)),
                ('event_type', models.CharField(blank=True, max_length=10, null=True, verbose_name='\u4e8b\u4ef6\u7c7b\u578b', choices=[(b'delete', '\u5220\u9664'), (b'add', '\u65b0\u589e'), (b'update', '\u66f4\u65b0')])),
                ('object_id', models.IntegerField(null=True, verbose_name='\u6570\u636eID', blank=True)),
                ('model_name', models.CharField(max_length=100, null=True, verbose_name='\u4fee\u6539\u5bf9\u8c61\u540d\u79f0', blank=True)),
                ('field_name', models.CharField(max_length=100, null=True, verbose_name='\u4fee\u6539\u7684\u5b57\u6bb5\u540d\u79f0', blank=True)),
                ('before_value', models.TextField(null=True, verbose_name='\u4fee\u6539\u524d\u7684\u503c', blank=True)),
                ('after_value', models.TextField(null=True, verbose_name='\u4fee\u6539\u540e\u7684\u503c', blank=True)),
                ('operator', models.CharField(max_length=100, null=True, verbose_name='\u64cd\u4f5c\u4eba', blank=True)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
