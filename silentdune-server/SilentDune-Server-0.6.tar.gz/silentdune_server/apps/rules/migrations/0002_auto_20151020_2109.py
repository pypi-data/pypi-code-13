# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rules', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='RuleBundle',
            new_name='Bundle',
        ),
        migrations.RemoveField(
            model_name='iptablesbundleset',
            name='bundlename',
        ),
        migrations.RemoveField(
            model_name='iptablesbundleset',
            name='iptables_chainset',
        ),
        migrations.DeleteModel(
            name='IPTablesBundleSet',
        ),
    ]
