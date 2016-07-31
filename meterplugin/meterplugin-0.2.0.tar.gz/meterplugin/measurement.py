#!/usr/bin/env python
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

from threading import Lock
from sys import stdout
import logging
from tspapi import API

logger = logging.getLogger(__name__)


class MeasurementSink(object):

    def __init__(self):
        pass

    def send(self, measurement):
        pass


class MeasurementSinkStandardOut(MeasurementSink):

    lock = Lock()

    def __init__(self):
        super(MeasurementSinkStandardOut, self).__init__()

    def send(self, measurement):
        """
        Sends a measurement to standard out to be received by Plugin manager
        :param measurement: Measurement to be sent to the Plugin manager
        :return: None
        """
        with MeasurementSinkStandardOut.lock:
            measurement = '{metric} {value} {source} {timestamp}'.format(
                metric=measurement.metric,
                value=measurement.value,
                source=measurement.source,
                timestamp=measurement.timestamp)
            print(measurement)
            logger.debug(measurement)
            stdout.flush()


class MeasurementSinkAPI(MeasurementSink):

    def __init__(self):
        super(MeasurementSinkAPI, self).__init__()
        self._api = API()

    def send(self, measurement):
        """
        Use TrueSight Pulse Python API to send measurement directly to back end
        :param measurement: Measurement to send via measurement API
        :return: None
        """
        self._api.measurement_create_batch([measurement])


class MeasurementSinkRPC(MeasurementSink):

    def send(self, measurement):
        """
        Use the Meter RPC channel to send measurement to the meter
        which will then forward to Pulse API Service
        :param measurement: Measurement to send via RPC channel
        :return: None
        """
        pass

