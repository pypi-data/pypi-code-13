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
from __future__ import print_function

from meterplugin import PluginParameters
import sys
import os
import logging
import argparse
from time import sleep

logger = logging.getLogger(__name__)


class PluginRunner(object):
    def __init__(self):
        self.module_name = None
        self.class_name = None
        self.meter_plugin = None
        self.parameters = PluginParameters()
        self.collectors = []
        self.levels = {"debug": logging.DEBUG,
                       "info": logging.INFO,
                       "warn": logging.WARN,
                       "error": logging.ERROR,
                       "critical": logging.CRITICAL}

    @staticmethod
    def usage():
        """
        Method to output the usage of plugin runner
        :return: None
        """
        sys.stderr.write("usage PluginRunner: <module name> <class name>\n")
        sys.exit(1)

    def load_plugin(self):
        """
        Dynamically load the class from the specified module that implements the Plugin
        :return:
        """
        sys.path.append(os.path.curdir)
        logger.debug('loading plugin: {0} from {1}'.format(self.class_name, self.module_name))
        module = __import__(self.module_name)
        class_ = getattr(module, self.class_name)
        meter_plugin = class_()
        meter_plugin.initialize()
        self.meter_plugin = meter_plugin

    def create_collectors(self):
        """
        Generate the collectors from each of the parameter items
        :return: None
        """

        for item in self.parameters.get_items():
            collector = self.meter_plugin.create_collector(item)
            self.collectors.append(collector)

    def start_collectors(self):
        """
        Spawn a thread for each collector
        :return:
        """
        for collector in self.collectors:
            collector.setDaemon(True)
            collector.start()

    def parse_arguments(self):
        parser = argparse.ArgumentParser(description='Plugin Runner')

        parser.add_argument('-l', '--log-level', dest='log_level', action='store', required=False,
                            choices=['debug', 'info', 'warning', 'error', 'critical'],
                            help='Sets logging level to one of debug,info,warning,error,critical. ' +
                                 'Default is logging is disabled')

        parser.add_argument('-c', '--class-name', dest='class_name', action='store',
                            required=True, metavar="class_name",
                            help='Name of the class that implements the plugin')

        parser.add_argument('-m', '--module-name', dest='module_name', action='store', default='plugin',
                            required=False, metavar="module_name",
                            help='Name of the module that contains the Plugin class')

        args = parser.parse_args()

        if args.log_level is not None:
            logging.basicConfig(stream=sys.stderr,
                            format='[%(levelname)s] (%(threadName)-s) %(message)s',
                            level=self.levels[args.log_level])

        self.class_name = args.class_name
        self.module_name = args.module_name

    def run(self):
        """
        1) Loads the class derived from Plugin
        2) Initializes and then runs Plugin
        :return: None
        """
        self.parse_arguments()
        self.parameters.load()
        self.load_plugin()
        self.meter_plugin.parameters_loaded(self.parameters)
        self.create_collectors()
        self.meter_plugin.starting()
        self.start_collectors()

        try:
            while True:
                sleep(0.1)
        except KeyboardInterrupt:
            for collector in self.collectors:
                collector.end()

            for collector in self.collectors:
                collector.join()


def main():
    """
    Entry point for running plugins
    :return: None
    """
    plugin_runner = PluginRunner()
    plugin_runner.run()


if __name__ == '__main__':
    main()
