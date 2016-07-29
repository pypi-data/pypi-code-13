# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fluentcms_button', '0002_buttonitem_align'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='buttonitem',
            name='block',
        ),
        migrations.AlterField(
            model_name='buttonitem',
            name='align',
            field=models.CharField(default=b'', max_length=50, verbose_name='Alignment', blank=True, choices=[(b'', 'Inline'), (b'left', 'Left'), (b'center', 'Center'), (b'right', 'Right'), (b'block', 'Full Width')]),
        ),
    ]
