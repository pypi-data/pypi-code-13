# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('iptables', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='IPTablesBundleSet',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
            ],
            options={
                'db_table': 'iptables_bundle_set',
            },
        ),
        migrations.CreateModel(
            name='RuleBundle',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('platform', models.CharField(choices=[('iptables', 'IPTables')], max_length=30, verbose_name='Firewall Platform')),
                ('name', models.CharField(max_length=50, verbose_name='Chain Set Name')),
                ('desc', models.CharField(default='', max_length=500, verbose_name='Description')),
                ('notes', models.CharField(default='', max_length=4000, verbose_name='Notes')),
            ],
            options={
                'db_table': 'rule_bundle',
            },
        ),
        migrations.AddField(
            model_name='iptablesbundleset',
            name='bundlename',
            field=models.ForeignKey(related_name='bundles', to='rules.RuleBundle'),
        ),
        migrations.AddField(
            model_name='iptablesbundleset',
            name='iptables_chainset',
            field=models.ForeignKey(related_name='chainsets', to='iptables.IPTablesChainSet'),
        ),
    ]
