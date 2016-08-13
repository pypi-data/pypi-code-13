# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FollowerInformation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('followers', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('polymorphic_ctype', models.ForeignKey(related_name='polymorphic_notifications.followerinformation_set+', editable=False, to='contenttypes.ContentType', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HasReadMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_read', models.BooleanField(default=False)),
                ('time', models.DateTimeField(null=True, blank=True)),
                ('is_removed', models.BooleanField(default=False)),
                ('notification_setting', models.CharField(max_length=20, choices=[(b'NO', 'No notifications'), (b'EM', 'Email only'), (b'IN', 'Internal only'), (b'ALL', 'Email and internal')])),
                ('email_sent', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now, editable=False, db_index=True)),
                ('modified', models.DateTimeField(default=django.utils.timezone.now, editable=False, db_index=True)),
                ('title', models.CharField(max_length=120)),
                ('notification', models.TextField()),
                ('is_removed', models.BooleanField(default=False)),
                ('recipients', models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='notifications.HasReadMessage')),
                ('user', models.ForeignKey(related_name='messages_sent', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NotificationSetting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('notification_type', models.CharField(default=b'ALL', max_length=20, choices=[(b'NO', 'No notifications'), (b'EM', 'Email only'), (b'IN', 'Internal only'), (b'ALL', 'Email and internal')])),
                ('user', models.OneToOneField(related_name='notification_setting', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='hasreadmessage',
            name='message',
            field=models.ForeignKey(related_name='has_read_messages', to='notifications.Notification'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='hasreadmessage',
            name='person',
            field=models.ForeignKey(related_name='messages_received', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='followerinformation',
            unique_together=set([('content_type', 'object_id')]),
        ),
    ]
