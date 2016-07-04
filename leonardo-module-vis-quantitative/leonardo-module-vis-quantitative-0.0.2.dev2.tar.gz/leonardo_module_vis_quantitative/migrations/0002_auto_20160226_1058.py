# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import yamlfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('leonardo_module_vis_quantitative', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='quantitativedata',
            options={'verbose_name': 'Quantitative data', 'verbose_name_plural': 'Quantitative data'},
        ),
        migrations.AlterModelOptions(
            name='quantitativedatasource',
            options={'verbose_name': 'Quantitative data source', 'verbose_name_plural': 'Quantitative data sources'},
        ),
        migrations.AlterField(
            model_name='quantitativedatasource',
            name='data',
            field=yamlfield.fields.YAMLField(help_text='For graphite set: host, port, ssl, user, passwd', verbose_name='data'),
        ),
    ]
