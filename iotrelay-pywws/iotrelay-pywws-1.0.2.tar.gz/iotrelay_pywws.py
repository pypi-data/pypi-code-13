'''
Copyright (c) 2016, Emmanuel Levijarvi
All rights reserved.
License BSD
'''
import logging
import datetime
from iotrelay import Reading
from pywws import DataStore

__version__ = "1.0.2"

logger = logging.getLogger(__name__)

# hours to look back for readings
DEFAULT_LOOKBACK = 2
READING_TYPE = 'weather'


class Poll(object):
    def __init__(self, config):
        self.keys = [k.strip() for k in config['series keys'].split(',')]
        self.data_store = config['data store']
        lookback = int(config.get('lookback', DEFAULT_LOOKBACK))
        hours = datetime.timedelta(hours=lookback)
        self.last_ts = datetime.datetime.utcnow() - hours

    def get_readings(self):
        for data in DataStore.data_store(self.data_store)[self.last_ts:]:
            if data['idx'] <= self.last_ts:
                continue
            self.last_ts = data['idx']
            for key in self.keys:
                if not data[key]:
                    continue
                yield Reading(READING_TYPE, data[key], data['idx'], key)
