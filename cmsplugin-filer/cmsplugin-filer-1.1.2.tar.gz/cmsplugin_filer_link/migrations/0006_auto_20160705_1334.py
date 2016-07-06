# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-05 17:34
from __future__ import unicode_literals

from django.db import migrations
import djangocms_attributes_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cmsplugin_filer_link', '0005_filerlinkplugin_link_attributes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filerlinkplugin',
            name='link_attributes',
            field=djangocms_attributes_field.fields.AttributesField(blank=True, default=dict, help_text='Optional. Adds HTML attributes to the rendered link.'),
        ),
    ]
