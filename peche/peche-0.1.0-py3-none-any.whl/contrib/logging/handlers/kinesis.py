#!/usr/bin/env python
# -*- coding: utf8 -*-

import json
from peche.logging.handlers import Handler


class KinesisHandler(Handler):

    def __init__(self, client, stream, partition_key=None,
                 partition_key_callable=lambda e: e.ctx.name):

        self.client = client
        self.stream = stream
        self.partition_key = partition_key
        self.partition_key_callable = partition_key_callable

    def on_event(self, event):
        payload = {
            'timestamp': str(event.timestamp),
            'level': event.level.name.lower(),
            'message': event.message,
            'name': event.ctx.name,
            'path': event.path,
            'function': event.function,
            'line_no': event.line_no,
            'tags': event.tags
        }

        partition_key = self.partition_key or \
            self.partition_key_callable(event)

        self.client.put_record(StreamName=self.stream,
                               Data=json.dumps(payload),
                               PartitionKey=partition_key)