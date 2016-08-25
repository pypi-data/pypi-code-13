# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='IPTablesChain',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(verbose_name='IPTables Table', max_length=15, choices=[('filter', 'Filter'), ('nat', 'Nat')])),
            ],
            options={
                'db_table': 'iptables_chain',
            },
        ),
        migrations.CreateModel(
            name='IPTablesChainSet',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('platform', models.CharField(default='iptables', verbose_name='Firewall Platform', max_length=30)),
                ('name', models.CharField(verbose_name='Chain Set Name', max_length=50)),
                ('desc', models.CharField(default='', verbose_name='Description', max_length=500)),
                ('notes', models.CharField(default='', verbose_name='Notes', max_length=4000)),
                ('slot', models.SmallIntegerField(choices=[(10, 'Administration'), (20, 'SD Server'), (30, 'Update Servers'), (40, 'User Defined')], verbose_name='Chain Set Slot')),
                ('sortId', models.SmallIntegerField(verbose_name='Sort ID')),
            ],
            options={
                'db_table': 'iptables_chainset',
            },
        ),
        migrations.CreateModel(
            name='IPTablesDestination',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('address', models.CharField(verbose_name='Address', max_length=255)),
                ('mask', models.SmallIntegerField(verbose_name='Mask')),
                ('invert', models.BooleanField(verbose_name='Invert')),
            ],
            options={
                'db_table': 'iptables_destination',
            },
        ),
        migrations.CreateModel(
            name='IPTablesFragment',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('fragment', models.BooleanField(default=False, verbose_name='Fragment')),
                ('invert', models.BooleanField(default=False, verbose_name='Invert')),
            ],
            options={
                'db_table': 'iptables_fragment',
            },
        ),
        migrations.CreateModel(
            name='IPTablesIFaceIn',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(verbose_name='Name', max_length=25)),
                ('invert', models.BooleanField(verbose_name='Invert')),
            ],
            options={
                'db_table': 'iptables_ifacein',
            },
        ),
        migrations.CreateModel(
            name='IPTablesIFaceOut',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(verbose_name='Name', max_length=25)),
                ('invert', models.BooleanField(verbose_name='Invert')),
            ],
            options={
                'db_table': 'iptables_ifaceout',
            },
        ),
        migrations.CreateModel(
            name='IPTablesJump',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('target', models.CharField(verbose_name='Target', max_length=50)),
            ],
            options={
                'db_table': 'iptables_jump',
            },
        ),
        migrations.CreateModel(
            name='IPTablesJumpOptions',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(verbose_name='Value', max_length=50)),
                ('value', models.CharField(verbose_name='Value', max_length=255)),
                ('jump', models.ForeignKey(related_name='params', to='iptables.IPTablesJump')),
            ],
            options={
                'db_table': 'iptables_jump_options',
            },
        ),
        migrations.CreateModel(
            name='IPTablesMatch',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(verbose_name='Value', max_length=50, choices=[('state', 'State')])),
            ],
            options={
                'db_table': 'iptables_match',
            },
        ),
        migrations.CreateModel(
            name='IPTablesMatchOptions',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('option', models.CharField(verbose_name='Option', max_length=50)),
                ('value', models.CharField(verbose_name='Value', max_length=1000)),
                ('invert', models.BooleanField(verbose_name='Invert')),
                ('matchName', models.ForeignKey(related_name='options', to='iptables.IPTablesMatch')),
            ],
            options={
                'db_table': 'iptables_match_options',
            },
        ),
        migrations.CreateModel(
            name='IPTablesProtocol',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(verbose_name='Name', max_length=25, choices=[('all', 'All'), ('tcp', 'tcp'), ('udp', 'udp'), ('icmp', 'icmp')])),
                ('invert', models.BooleanField(verbose_name='Invert')),
            ],
            options={
                'db_table': 'iptables_protocol',
            },
        ),
        migrations.CreateModel(
            name='IPTablesRing',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(verbose_name='IPTables Table Chain', max_length=15, choices=[('input', 'Input'), ('output', 'Output'), ('forward', 'Forward'), ('prerouting', 'Pre-Routing'), ('postrouting', 'Post-Routing')])),
                ('version', models.CharField(verbose_name='Transport Version', max_length=4, choices=[(1, 'ipv4'), (2, 'ipv6')])),
                ('chain', models.ForeignKey(related_name='rings', to='iptables.IPTablesChain')),
            ],
            options={
                'db_table': 'iptables_ring',
            },
        ),
        migrations.CreateModel(
            name='IPTablesRule',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('enabled', models.BooleanField(verbose_name='Enabled')),
                ('sortId', models.SmallIntegerField(verbose_name='Sort ID')),
                ('desc', models.CharField(default='', verbose_name='Description', max_length=500)),
                ('ring', models.ForeignKey(related_name='rules', to='iptables.IPTablesRing')),
            ],
            options={
                'db_table': 'iptables_rule',
            },
        ),
        migrations.CreateModel(
            name='IPTablesSource',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('address', models.CharField(verbose_name='Address', max_length=255)),
                ('mask', models.SmallIntegerField(verbose_name='Mask')),
                ('invert', models.BooleanField(verbose_name='Invert')),
                ('rule', models.ForeignKey(related_name='source', to='iptables.IPTablesRule')),
            ],
            options={
                'db_table': 'iptables_source',
            },
        ),
        migrations.AddField(
            model_name='iptablesprotocol',
            name='rule',
            field=models.ForeignKey(related_name='protocol', to='iptables.IPTablesRule'),
        ),
        migrations.AddField(
            model_name='iptablesmatch',
            name='rule',
            field=models.ForeignKey(related_name='matches', to='iptables.IPTablesRule'),
        ),
        migrations.AddField(
            model_name='iptablesjump',
            name='rule',
            field=models.OneToOneField(related_name='jump', to='iptables.IPTablesRule'),
        ),
        migrations.AddField(
            model_name='iptablesifaceout',
            name='rule',
            field=models.OneToOneField(related_name='ifaceOut', to='iptables.IPTablesRule'),
        ),
        migrations.AddField(
            model_name='iptablesifacein',
            name='rule',
            field=models.OneToOneField(related_name='ifaceIn', to='iptables.IPTablesRule'),
        ),
        migrations.AddField(
            model_name='iptablesfragment',
            name='rule',
            field=models.ForeignKey(related_name='fragment', to='iptables.IPTablesRule'),
        ),
        migrations.AddField(
            model_name='iptablesdestination',
            name='rule',
            field=models.ForeignKey(related_name='destination', to='iptables.IPTablesRule'),
        ),
        migrations.AddField(
            model_name='iptableschain',
            name='chainset',
            field=models.ForeignKey(related_name='chains', to='iptables.IPTablesChainSet'),
        ),
    ]
