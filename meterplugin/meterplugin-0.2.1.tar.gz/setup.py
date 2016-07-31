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
from distutils.core import setup
from meterplugin import __version__

setup(
    name='meterplugin',
    version=__version__,
    url='https://github.com/boundary/meter-plugin-sdk-python',
    author='David Gwartney',
    author_email='david_gwartney@bmc.com',
    packages=['meterplugin', ],
    entry_points={
        'console_scripts': [
            'plugin-runner = meterplugin.plugin_runner:main',
            'post-extract = meterplugin.post_extract:main',
        ],
    },
    package_data={'meterplugin': ['templates/*']},
    license='LICENSE',
    description='TrueSight Pulse Meter Plugin SDK for Python',
    long_description=open('README.txt').read(),
    install_requires=['tinyrpc', 'tspapi',],
    setup_requires=['tinyrpc', 'tspapi', ],
)
