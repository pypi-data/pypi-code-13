# -*- coding: utf-8 -*-
"""
    pip_services_runtime.run.Microservice
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Microservice container implementation
    
    :copyright: Digital Living Software Corp. 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from ..config.ConfigReader import ConfigReader
from ..config.MicroserviceConfig import MicroserviceConfig
from ..config.Category import Category
from ..build.Builder import Builder
from ..logs.LogFormatter import LogFormatter
from ..LogLevel import LogLevel
from .LogWriter import LogWriter
from .LifeCycleManager import LifeCycleManager

class Microservice(object):
    _name = None
    _factory = None
    _config = None
    _components = None

    def __init__(self, name, factory):
        self._factory = factory
        self._name = name

    def get_name(self):
        return self._name

    def get_config(self):
        return self._config

    def set_config(self, config):
        self._config = config

    def load_config(self, path):
        self._config = ConfigReader.read(path)

    def get_components(self):
        return self._components

    def fatal(self, *message):
        LogWriter.fatal( \
            self._components.get_all_by_category(Category.Logs), \
            LogFormatter.format(LogLevel.Fatal, message) \
        )

    def error(self, *message):
        LogWriter.error( \
            self._components.get_all_by_category(Category.Logs), \
            LogFormatter.format(LogLevel.Error, message) \
        )

    def info(self, *message):
        LogWriter.info( \
            self._components.get_all_by_category(Category.Logs), \
            LogFormatter.format(LogLevel.Info, message) \
        )

    def trace(self, *message):
        LogWriter.trace( \
            self._components.get_all_by_category(Category.Logs), \
            LogFormatter.format(LogLevel.Trace, message) \
        )

    def _build(self):
        self._components = Builder.build(self._factory, self._config)

    def _link(self):
        self.trace("Initializing " + self._name + " microservice")
        LifeCycleManager.link(self._components)

    def _open(self):
        self.trace("Opening " + self._name + " microservice")
        LifeCycleManager.open(self._components)
        self.info("Microservice " + self._name + " started")

    def start(self):
        self._build()
        self._link()
        self._open()

    def start_with_config(self, config):
        self.set_config(config)
        self.start()

    def start_with_config_file(self, config_path):
        self.load_config(config_path)
        self.start()

    def stop(self):
        self.trace("Closing " + self._name + " microservice")
        LifeCycleManager.force_close(self._components)
        self.info("Microservice " + self._name + " closed")
