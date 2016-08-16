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

import logging
from meterplugin import Collector

logger = logging.getLogger(__name__)


class Plugin(object):
    
    def __init__(self):
        pass

    def initialize(self):
        logger.debug('initialize()')

    def parameters_loaded(self, parameters):
        logger.debug('parameters_loaded()')

    def starting(self):
        logger.debug('starting()')

    def create_collector(self, item):
        logger.debug('create_collector()')
        return Collector()

    def run(self):
        pass

