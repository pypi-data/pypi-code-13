#
# Copyright 2016 BMC Software, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from __future__ import print_function

import logging
from sys import stderr
from time import sleep
from threading import Thread, Event
from meterplugin import EventSinkStandardOut
from meterplugin import MeasurementSinkStandardOut

logger = logging.getLogger(__name__)


class Collector(Thread):

    def __init__(self, interval=1000, name=None):
        super(Collector, self).__init__(name=name)
        self.interval = interval / 1000.0
        self.event_output = EventSinkStandardOut()
        self.measurement_output = MeasurementSinkStandardOut()
        self.run_event = Event()
        self.run_event.set()

    def run(self):
        """
        Called by thread to perform collection of measurements
        :return:  None
        """
        while self.run_event.is_set():
            self.collect()
            sleep(self.interval)

    def initialize(self):
        """
        Default initialze method, sub-classes override as needed
        :return: None
        """
        logger.debug('initialize()')

    def begin(self):
        """
        Default start method, sub-classes override if needed to
        be signalled before running
        :return:
        """
        logger.debug('start()')

    def collect(self):
        """
        Default collection method, sub-classes need to override to do anything useful
        :return: None
        """
        logger.debug('collect()')

    def end(self):
        self.run_event.clear()

