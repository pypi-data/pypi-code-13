'''
Copyright (c) 2016, Emmanuel Levijarvi
All rights reserved.
License BSD
'''
import logging
import datetime
from pytz import timezone, reference
from iotrelay import Reading
import nest

logger = logging.getLogger(__name__)
__version__ = "1.0.0"


class Poll(object):
    def __init__(self, config):
        # poll_frequency: seconds between readings
        poll_frequency = int(config['poll frequency'])
        localtime = reference.LocalTimezone()
        tzname = localtime.tzname(datetime.datetime.now())
        self.timezone = timezone(config.get('timezone', tzname))
        self.delta = datetime.timedelta(seconds=poll_frequency)
        self.next_reading_time = datetime.datetime.now()
        self.nest = nest.Nest(config['username'], config['password'])
        self.nest.login()
        self.last_timestamp = None

    def get_readings(self):
        if datetime.datetime.now() > self.next_reading_time:
            self.nest.get_status()
            self.next_reading_time = datetime.datetime.now() + self.delta
            timestamp = self.nest.status['shared'][self.nest.serial]['$timestamp']
            if self.last_timestamp is None or timestamp > self.last_timestamp:
                self.last_timestamp = timestamp
                timestamp = datetime.datetime.fromtimestamp(timestamp/1000, self.timezone)
                timestamp = timestamp.astimezone(timezone('UTC'))
                temp = self.nest.status['shared'][self.nest.serial]['current_temperature']
                logger.debug('nest temp: {0}'.format(temp))
                yield Reading('weather', temp, timestamp, series_key='nest_temp')
                hum = self.nest.status["device"][self.nest.serial]["current_humidity"]
                logger.debug('nest hum: {0}'.format(hum))
                yield Reading('weather', hum, timestamp, series_key='nest_hum')
