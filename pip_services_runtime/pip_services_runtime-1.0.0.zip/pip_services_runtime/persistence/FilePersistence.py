# -*- coding: utf-8 -*-
"""
    pip_services_runtime.persistence.FilePersistence
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Abstract file-based persistence implementation
    
    :copyright: Digital Living Software Corp. 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import json
import random
import os.path

from .AbstractPersistence import AbstractPersistence
from ..State import State
from ..portability.DynamicMap import DynamicMap
from ..portability.Converter import Converter
from ..data.PagingParams import PagingParams
from ..data.DataPage import DataPage
from ..errors.ConfigError import ConfigError
from ..errors.FileError import FileError

filtered = filter

class FilePersistence(AbstractPersistence):
    """
    Abstract file-based implementation of microservice persistence components
    that store and retrieve persistent data.
    """

    _default_config = DynamicMap.from_tuples( \
        "options.max_page_size", 100 \
    )

    _path = None
    _initial_data = None
    _max_page_size = None
    _items = None

    def __init__(self, descriptor):
        """
        Creates instance of abstract file persistence component.
        
        Args:
            descriptor: the unique descriptor that is used to identify and locate the component.
        """
        super(FilePersistence, self).__init__(descriptor)

    def configure(self, config):
        """
        Sets component configuration parameters and switches from component
        to 'Configured' state. The configuration is only allowed once
        right after creation. Attempts to perform reconfiguration will cause an exception.
        
        Args:
            config: the component configuration parameters.

        Returns: None

        Args:
            MicroserviceError: when component is in illegal state or configuration validation fails. 
        """
        self.check_new_state_allowed(State.Configured)
        
        config = config.with_defaults(self._default_config)
        options = config.get_options()
        
        if options == None or options.has_not("path"):
            raise ConfigError(self, "NoPath", "Data file path is not set")
        
        super(FilePersistence, self).configure(config)

        self._path = options.get_string("path")
        self._max_page_size = options.get_integer("max_page_size")
        self._initial_data = options.get("data")

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
        
        # Fill with predefined data (for testing)
        if type(self._initial_data) in [list, tuple]:
            self._items = list(self._initial_data)
        else:
            self.load()

        super(FilePersistence, self).open()

    def close(self):
        """
        Closes the component and all open connections, performs deinitialization
        steps. Closure can only be done from opened state. Attempts to close
        already closed component or in wrong order will cause exception.
        
        Returns: None
        
        Raises:
            MicroserviceError: with closure fails.
        """
        self.check_new_state_allowed(State.Closed)

        self.save()
        
        super(FilePersistence, self).close()

    def load(self):
        self.trace(None, "Loading data from file at " + self._path)

        # If doesn't exist then consider empty data
        if not os.path.isfile(self._path):
            self._items = []
            return

        try:
            with open(self._path, 'r') as file:
                self._items = json.load(file)
        except Exception as e:
            raise FileError(self, "ReadFailed", "Failed to read data file") \
                .with_cause(e)

    def save(self):
        self.trace(None, "Saving data to file at " + self._path)

        try:
            with open(self._path, 'w') as file:
                json.dump(self._items, file)
        except Exception as e:
            raise FileError(self, "WriteFailed", "Failed to write data file") \
                .with_cause(e)

    def clear_test_data(self):
        self._items = []
        self.save()

    def get_page(self, correlation_id, filter_func, paging, sort_func = None, select_func = None):
        items = self._items
        
        # Filter and sort
        if filter_func != None:
            items = filtered(filter_func, items)
        if sort_func != None:
            items = sorted(items, sort_func)

        # Prepare paging parameters        
        paging = paging if paging != None else PagingParams()
        skip = paging.get_skip(-1)
        take = paging.get_take(self._max_page_size)
        
        # Get a page
        page_items = items
        if skip > 0:
            page_items = page_items[skip:]
        if take > 0:
            page_items = page_items[:take+1]
                
        # Convert values
        if select_func != None:
            page_items = map(select_func, page_items)
                
        # Return a page
        return DataPage(page_items, len(items))

    def get_list(self, correlation_id, filter_func, sort_func = None, select_func = None):
        items = self._items

        # Filter and sort        
        if filter_func != None:
            items = filtered(items, filter_func)
        if sort_func != None:
            items = sorted(items, sort_func) 
                          
        # Convert values      
        if select_func != None:
            items = map(select_func, items)
                
        # Return a list
        return items

    def get_by_id(self, correlation_id, id):
        for item in self._items:
            if item['id'] == id:
                return item

        return None

    def get_random(self, correlation_id):
        if len(self._items) == 0: return None

        index = random.randint(0, length(_items))
        return self._items[index]

    def create(self, correlation_id, item):
        item = dict(item)
        item['id'] = item['id'] if 'id' in item and item['id'] != None else self.create_uuid()

        self._items.append(item)

        self.save()
        return item

    def replace(self, correlation_id, id, new_item):
        item = self.get_by_id(correlation_id, id)
        if item == None: return None
        
        index = self._items.index(item)
        if index < 0: return None

        new_item['id'] = id
        self._items[index] = new_item

        self.save()
        return new_item

    def update(self, correlation_id, id, new_values):
        if not isinstance(new_values, DynamicMap):
            new_values = Converter.to_nullable_map(new_values)

        item = self.get_by_id(correlation_id, id)
        if item == None: return None

        new_values.assign_to(item)

        self.save()
        return item

    def delete(self, correlation_id, id):
        item = self.get_by_id(correlation_id, id)
        if item == None: return
        
        index = self._items.index(item)
        if index < 0:
            return

        del self._items[index]

        self.save()
