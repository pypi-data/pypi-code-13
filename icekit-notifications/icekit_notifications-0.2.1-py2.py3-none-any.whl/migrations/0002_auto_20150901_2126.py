# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='followerinformation',
            name='group_followers',
            field=models.ManyToManyField(to='auth.Group', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='followerinformation',
            name='followers',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, blank=True),
            preserve_default=True,
        ),
    ]
