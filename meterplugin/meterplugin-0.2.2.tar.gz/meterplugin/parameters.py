# Copyright 2015 BMC Software, Inc.
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

import json
from pprint import pprint
import logging
import StringIO

logger = logging.getLogger(__name__)


class PluginParameters:

    def __init__(self, path='param.json'):
        """
        Initialize class members
        :param path:
        """
        self.config = None
        self.path = path

    def get_entry_count(self):
        """
        Returns the number of configuration items
        :return:
        """
        return len(self.config['items'])

    def load(self):
        """
        Load the param.json file
        :return:
        """
        with open(self.path) as f:
            data = json.load(f)
            # Loop over the items and put into list
            self.config = data

    def __str__(self):
        """
        Output the parameters as a string
        :return:
        """
        output = StringIO.StringIO()
        pprint(self.config, stream=output)
        return output.getvalue()

    def get_items(self):
        return self.config['items'] if self.config is not None else None

