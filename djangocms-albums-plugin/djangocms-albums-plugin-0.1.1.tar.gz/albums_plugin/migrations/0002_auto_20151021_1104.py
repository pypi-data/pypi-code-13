# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('albums_plugin', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AlbumSet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250)),
                ('description', models.TextField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='photo',
            name='is_album_cover',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='photoalbum',
            name='albumset',
            field=models.ForeignKey(related_name='albums', default=1, to='albums_plugin.AlbumSet'),
            preserve_default=False,
        ),
    ]
