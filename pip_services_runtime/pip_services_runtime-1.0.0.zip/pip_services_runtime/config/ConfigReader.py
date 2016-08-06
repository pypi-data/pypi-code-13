# -*- coding: utf-8 -*-
"""
    pip_services_runtime.config.ConfigReader
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Configuration reader implementation
    
    :copyright: Digital Living Software Corp. 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import os.path
import json 
import yaml

from ..errors.FileError import FileError
from ..portability.DynamicMap import DynamicMap
from .MicroserviceConfig import MicroserviceConfig 

class ConfigReader(object):
    """
    Configuration reader capable of reading various formats:
    JavaScript, JSON, YAML, XML, etc.
    """

    @staticmethod
    def read(file_path):
        """
        Reads configuration from a file.
        The file type is automatically determined by its extension
        
        Args:
            file_path: a path to configuration file.

        Returns: MicroserviceConfig with file content

        Throws:
            FileError: when file wasn't found or reading failed
        """
        # Check if config file is present
        if not os.path.isfile(file_path):
            raise FileError('FileNotFound', 'Config file was not found at ' + file_path)

        root, ext = os.path.splitext(file_path)
        ext = ext.lower()

        if ext == '.json':
            return ConfigReader.read_json(file_path)
        elif ext == '.yaml':
            return ConfigReader.read_yaml(file_path)

        # By default read as JSON
        return ConfigReader.read_json(file_path)

    @staticmethod
    def read_json(file_path):
        """
        Reads configuration from JSON file.
        The file type is automatically determined by its extension
        
        Args:
            file_path: a path to configuration file.

        Returns: MicroserviceConfig with file content

        Throws:
            FileError: when file wasn't found or reading failed
        """
        # Check if config file is present
        if not os.path.isfile(file_path):
            raise FileError('FileNotFound', 'Config file was not found at ' + file_path)

        try:
            with open(file_path, 'r') as file:
                content = json.load(file)
                return MicroserviceConfig.from_value(content)
        except Exception as e:
            raise FileError( \
                'ReadFailed', \
                'Failed reading configuration from ' + file_path + ': ' + str(e) \
            ) \
            .with_details(file_path) \
            .wrap(e)

    @staticmethod
    def read_yaml(file_path):
        """
        Reads configuration from YAML file.
        The file type is automatically determined by its extension
        
        Args:
            file_path: a path to configuration file.

        Returns: MicroserviceConfig with file content

        Throws:
            FileError: when file wasn't found or reading failed
        """
        # Check if config file is present
        if not os.path.isfile(file_path):
            raise FileError('FileNotFound', 'Config file was not found at ' + file_path)

        try:
            with open(file_path, 'r') as file:
                content = yaml.load(file)
                return MicroserviceConfig.from_value(content)
        except Exception as e:
            raise FileError( \
                'ReadFailed', \
                'Failed reading configuration from ' + file_path + ': ' + str(e) \
            ) \
            .with_details(file_path) \
            .wrap(e)
