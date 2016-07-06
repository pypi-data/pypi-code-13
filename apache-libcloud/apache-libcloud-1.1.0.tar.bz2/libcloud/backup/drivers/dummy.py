# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from libcloud.backup.base import BackupDriver


class DummyBackupDriver(BackupDriver):
    """
    Dummy Backup driver.

    >>> from libcloud.backup.drivers.dummy import DummyBackupDriver
    >>> driver = DummyBackupDriver('key', 'secret')
    >>> driver.name
    'Dummy Backup Provider'
    """

    name = 'Dummy Backup Provider'
    website = 'http://example.com'

    def __init__(self, api_key, api_secret):
        """
        :param    api_key:    API key or username to used (required)
        :type     api_key:    ``str``

        :param    api_secret: Secret password to be used (required)
        :type     api_secret: ``str``

        :rtype: ``None``
        """
