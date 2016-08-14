#
# Copyright 2016 BMC Software, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from distutils.core import setup

setup(
    name='tspapi',
    version='0.3.6',
    url="https://github.com/boundary/pulse-api-python",
    author='David Gwartney',
    author_email='david_gwartney@bmc.com',
    packages=['tspapi', ],
    license='Apache 2',
    description='Python Bindings for the TrueSight Pulse REST APIs',
    long_description=open('README.txt').read(),
    entry_points={
        'console_scripts': [
            'api-logviewer = tspapi.logviewer:main'
        ]
    },
    install_requires=[
        "requests >= 2.3.0",
        "six >= 1.10.0",
        "python-dateutil >= 2.5.2",
    ],
)
