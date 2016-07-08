# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import repositories.custom_models


class Migration(migrations.Migration):

    dependencies = [
        ('integration', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Webhook',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('model_selected', models.CharField(max_length=50, db_column=b'webhoook_model_selected')),
                ('external_id', models.BigIntegerField(db_column=b'webhook_external_id')),
                ('account_id', models.BigIntegerField(db_column=b'webhook_account_id')),
                ('contract_id', models.BigIntegerField(db_column=b'webhook_contract_id')),
                ('message_body', models.TextField(null=True, db_column=b'webhook_message_body', blank=True)),
                ('response', models.TextField(null=True, db_column=b'webhook_web_response', blank=True)),
                ('status', models.CharField(default=b'WAIT', max_length=35, db_column=b'webhook_status', choices=[('WAIT', 'Aguardando envio para {}'), ('QUEUE', 'Em fila para {}'), ('RETRY', 'Nova tentativa para {}'), ('SUCCESS', 'Integrado com sucesso para {}'), ('FAIL', '{} n\xe3o aceitou os dados'), ('ERROR', 'Ocorreu um erro no envio'), ('NO CHANGES', 'Nenhum dado foi alterado')])),
                ('access_key', repositories.custom_models.UUIDField(max_length=64, db_column=b'webhook_access_key', blank=True)),
                ('integration', models.ForeignKey(related_name='integration_webhook', db_column=b'integration_id', to='integration.Integration')),
            ],
            options={
                'db_table': 'integration"."tb_webhook',
                'verbose_name': 'Webhook',
                'verbose_name_plural': 'Webhooks',
            },
        ),
    ]
