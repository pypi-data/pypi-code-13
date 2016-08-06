# -*- coding: utf-8 -*-
"""
    pip_services_runtime.boot.FileBootConfig
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    File boot configuration reader component implementation
    
    :copyright: Digital Living Software Corp. 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import os.path

from .AbstractBootConfig import AbstractBootConfig
from ..State import State

from ..errors.ConfigError import ConfigError
from ..errors.FileError import FileError

from ..config.Category import Category
from ..config.ComponentDescriptor import ComponentDescriptor
from ..config.ConfigReader import ConfigReader
from ..config.MicroserviceConfig import MicroserviceConfig

FileBootConfigDescriptor = ComponentDescriptor( \
    Category.Boot, "pip-services-runtime-boot", "file", "*" \
)
"""
Unique descriptor for the FileBootConfig component
"""

class FileBootConfig(AbstractBootConfig):
    """
    Boot configuration reader that gets microservice configuration from JSON file on local disk. 
    
    This is the simplest possible configuration.
    However, in large scale deployments it may be unpractical. 
    The distrubuting configurations from a centralized configuration 
    repository may be a better option. Check other types of readers to support those scenarios.
    """

    _path = None

    def __init__(self):
        """
        Creates an instance of file configuration reader component.
        """
        super(FileBootConfig, self).__init__(FileBootConfigDescriptor)

    def configure(self, config):
        """
        Sets component configuration parameters and switches from component
        to 'Configured' state. The configuration is only allowed once
        right after creation. Attempts to perform reconfiguration will  cause an exception.

        Args:
            config: the component configuration parameters.

        Returns: None

        Raises:
            MicroserviceError: when component is in illegal state or configuration validation fails. 
        """
        self.check_new_state_allowed(State.Configured)

        options = config.get_options()
        if options == None or options.has_not("path"):
            raise ConfigError(self, "NoPath", "Missing config file path")
        
        super(FileBootConfig, self).configure(config)
        
        self._path = options.get_string("path")

    def open(self):
        """
        Opens the component, performs initialization, opens connections
        to external services and makes the component ready for operations.
        Opening can be done multiple times: right after linking or reopening after closure.  
        
        Returns: None

        Raises:
            MicroserviceError: when initialization or connections fail.
        """
        self.check_new_state_allowed(State.Opened)
        
        if not os.path.isfile(self._path):
            raise FileError('FileNotFound', 'Config file was not found at ' + self._path) \
                .with_details(self._path)

        super(FileBootConfig, self).open()

    def read_config(self):
        """
        Reads microservice configuration from the source

        Returns: a MicroserviceConfiguration object
        
        Raises:
            MicroserviceError: when reading fails for any reason
        """
        return ConfigReader.read(self._path)

FileBootConfig.Descriptor = FileBootConfigDescriptor
