# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import filer.fields.image


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0013_urlconfrevision'),
        ('filer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Section',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('headline', models.CharField(max_length=512, verbose_name='headline', blank=True)),
                ('image_caption', models.CharField(max_length=512, verbose_name='image caption', blank=True)),
                ('style', models.CharField(default='default', max_length=50, verbose_name='style', choices=[('default', 'Default')])),
                ('image', filer.fields.image.FilerImageField(related_name='section', verbose_name='image', to='filer.Image')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
    ]
