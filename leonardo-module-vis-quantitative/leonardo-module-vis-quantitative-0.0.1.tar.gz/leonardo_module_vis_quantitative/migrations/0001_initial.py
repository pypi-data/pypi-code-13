# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='QuantitativeData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('metrics', models.TextField(verbose_name='metrics')),
            ],
            options={
                'verbose_name': 'Quatitative data',
                'verbose_name_plural': 'Quatitative data',
            },
        ),
        migrations.CreateModel(
            name='QuantitativeDataSource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(default=b'graphite', max_length=255, verbose_name='type', choices=[(b'graphite', 'Graphite')])),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('data', models.TextField(help_text='For graphite set: host, port, ssl, user, passwd', verbose_name='data')),
            ],
            options={
                'verbose_name': 'Quatitative data source',
                'verbose_name_plural': 'Quatitative data sources',
            },
        ),
        migrations.AddField(
            model_name='quantitativedata',
            name='data_source',
            field=models.ForeignKey(verbose_name='data source', to='leonardo_module_vis_quantitative.QuantitativeDataSource'),
        ),
        migrations.AlterField(
            model_name='quantitativedatasource',
            name='type',
            field=models.CharField(default=b'graphite', max_length=255, verbose_name='type', choices=[(b'dummy', 'Test data'), (b'graphite', 'Graphite'), (b'influxdb', 'InfluxDB'), (b'opentsdb', 'OpenTSDB')]),
        ),
    ]
