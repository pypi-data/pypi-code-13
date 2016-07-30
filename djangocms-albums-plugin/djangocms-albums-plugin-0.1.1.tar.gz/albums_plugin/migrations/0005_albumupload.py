# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('albums_plugin', '0004_albumsplugin'),
    ]

    operations = [
        migrations.CreateModel(
            name='AlbumUpload',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('zip_file', models.FileField(upload_to=b'temp/')),
                ('new_album_name', models.CharField(max_length=250, null=True, blank=True)),
                ('album', models.ForeignKey(blank=True, to='albums_plugin.PhotoAlbum', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
