# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import uuid
import os


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SoundFile',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, serialize=False, primary_key=True)),
                ('file', models.FileField(upload_to=os.path.join(settings.BASE_DIR, 'generated'))),
                ('text', models.TextField()),
                ('command', models.CharField(max_length=255, blank=True)),
                ('type', models.CharField(max_length=5, choices=[(b'wav', b'wav')])),
                ('dc', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
    ]
