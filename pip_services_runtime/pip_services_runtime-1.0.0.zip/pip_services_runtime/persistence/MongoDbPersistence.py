# -*- coding: utf-8 -*-
"""
    pip_services_runtime.persistence.MongoDbPersistence
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Abstract mongodb-based persistence implementation
    
    :copyright: Digital Living Software Corp. 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import random
import pymongo

from .AbstractPersistence import AbstractPersistence
from ..State import State
from ..portability.DynamicMap import DynamicMap
from ..portability.Converter import Converter
from ..data.PagingParams import PagingParams
from ..data.DataPage import DataPage
from ..errors.ConfigError import ConfigError
from ..errors.ConnectionError import ConnectionError
from ..errors.CallError import CallError

class MongoDbPersistence(AbstractPersistence):
    """
    Abstract mongodb-based implementation of microservice persistence components
    that store and retrieve persistent data.
    """

    _default_config = DynamicMap.from_tuples( \
        "connection.type", "mongodb", \
        "connection.host", "localhost", \
        "connection.port", 27017, \
        # "connection.database", None, \
        # "connection.username", None, \
        # "connection.password", None, \
        "options.server.pollSize", 4, \
        "options.server.socketOptions.keepAlive", 1, \
        "options.server.socketOptions.connectTimeoutMS", 5000, \
        "options.server.auto_reconnect", True, \
        "options.max_page_size", 100, \
        "options.debug", True \
    )

    _client = None
    _db_name = None
    _db = None
    _collection_name = None
    _collection = None
    _max_page_size = None
    _converter = None
    _list_converter = None

    def __init__(self, descriptor, collection_name = None):
        """
        Creates instance of abstract mongodb persistence component.
        
        Args:
            descriptor: the unique descriptor that is used to identify and locate the component.
            collection_name: the name of collection to read and write
        """
        super(MongoDbPersistence, self).__init__(descriptor)
        self._collection_name = collection_name

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
        connection = config.get_connection()
        options = config.get_options()
        
        if connection == None:
            raise ConfigError(self, "NoConnection", "Database connection is not set")

        if connection.get_type() != "mongodb":
            raise ConfigError(self, "WrongType", "Mongodb is the only supported connection type")
        
        if connection.get_host() == None:
            raise ConfigError(self, "NoHost", "Connection host is not set")

        if connection.get_port() == None:
            raise ConfigError(self, "NoPort", "Connection port is not set")

        if connection.get_database() == None:
            raise ConfigError(self, "NoDatabase", "Connection database is not set")

        super(MongoDbPersistence, self).configure(config)

        self._converter = self._convert_item
        self._list_converter = self._convert_list_item

        self._db_name = connection.get_database()        
        self._max_page_size = options.get_integer("max_page_size")

    def open(self):
        """
        Opens the component, performs initialization, opens connections
        to external services and makes the component ready for operations.
        Opening can be done multiple times: right after linking or reopening after closure.

        Returns: None  
        """
    	self.check_new_state_allowed(State.Opened)

        connection = self._config.get_connection()
        host = connection.get_host()
        port = connection.get_port()
        username = connection.get_username()
        password = connection.get_password()
        uri = connection.get_uri()

        options = self._config.get_options()
        self.trace(None, 'Connecting to mongodb at ' + uri)

        try:
            self._client = pymongo.MongoClient(host, port)

            self._db = self._client[self._db_name]
            if username != None:
                 self._db.authenticate(username, password)

            self._collection = self._db[self._collection_name]
        except Exception as e:
            raise ConnectionError(self, 'ConnectFailed', 'Connection to mongodb failed: ' + str(e)) \
                .wrap(e)

        super(MongoDbPersistence, self).open()
    
    def close(self):
        """
        Closes the component and all open connections, performs deinitialization
        steps. Closure can only be done from opened state. Attempts to close
        already closed component or in wrong order will cause exception.

        Returns: None
        """
        self.check_new_state_allowed(State.Closed)

        try:
            if self._client != None:
                self._client.close()

            self._collection = None
            self._db = None
            self._client = None
        except Exception as e:
            raise ConnectionError(self, 'DisconnectFailed', 'Disconnect from mongodb failed: ' + str(e)) \
                .wrap(e)

        super(MongoDbPersistence, self).close()

    def clear_test_data(self):
        self._client.drop_database(self._db_name)

    def _convert_item(self, value):
        if value == None: return None

        value['id'] = value['_id']
        value.pop('_id', None)

        return value

    def _convert_list_item(self, value):
        if value == None: return None

        value['id'] = value['_id']
        value.pop('_id', None)
        value.pop('custom_dat', None)

        return value

    def get_page(self, correlation_id, filter, paging, sort, select):
        # Adjust max item count based on configuration
        paging = paging if paging != None else PagingParams()
        skip = paging.get_skip(-1)
        take = paging.get_take(self._max_page_size)
        paging_enabled = paging.is_total()

        try:
            # Configure statement
            statement = self._collection.find(filter)

            if skip >= 0:
                statement = statement.skip(skip)
            statement = statement.limit(take)
            if sort != None:
                statement = statement.sort(sort)
            if select != None:
                statement = statement.select(select)

            # Retrive page items
            items = []
            for item in statement:
                if self._list_converter != None:
                    item = self._list_converter(item)
                items.append(item)

            # Calculate total if needed
            total = None
            if paging_enabled:
                total = self._collection.find(filter).count()
        
        except Exception as e:
            raise CallError(self, 'ReadFailed', 'Reading page from database failed: ' + str(e)) \
                .with_correlation_id(correlation_id).wrap(e)
        
        return DataPage(items, total)

    def get_list(self, correlation_id, filter, sort, select):
        try:
            # Configure statement
            statement = self._db.find(filter)

            if sort != None:
                statement = statement.sort(sort)
            if select != None:
                statement = statement.select(select)

            # Retrive page items
            items = []
            for item in statement:
                if self._list_converter != None:
                    item = self._list_converter(item)
                items.append(item)

            return items
        except Exception as e:
            raise CallError(self, 'ReadFailed', 'Reading list from database failed: ' + str(e)) \
                .with_correlation_id(correlation_id).wrap(e)

    def get_random(self, correlation_id, filter):
        try:
            count = self._connection.find(filter).count()

            pos = random.randint(0, count)

            statement = self._connection.find(filter).skip(pos).limit(1)
            for item in statement:
                if self._converter != None:
                    item = self._converter(item)
                return item

            return None
        except Exception as e:
            raise CallError(self, 'ReadFailed', 'Reading item from database failed: ' + str(e)) \
                .with_correlation_id(correlation_id).wrap(e)

    def get_by_id(self, correlation_id, id):
        try:
            item = self._collection.find_one({ '_id': id })
            if self._converter != None:
                item = self._converter(item)
            return item
        except Exception as e:
            raise CallError(self, 'ReadFailed', 'Reading item from database failed: ' + str(e)) \
                .with_correlation_id(correlation_id).wrap(e)

    def create(self, correlation_id, item):
        new_item = dict(item)

        # Replace _id or generate a new one
        new_item.pop('_id', None)            
        new_item['_id'] = item['id'] if 'id' in item and item['id'] != None else self.create_uuid()

        try:
            result = self._collection.insert_one(new_item)
            item = self._collection.find_one({ '_id': result.inserted_id })
            if self._converter != None:
                item = self._converter(item)
            return item
        except Exception as e:
            raise CallError(self, 'CreateFailed', 'Creating item in database failed: ' + str(e)) \
                .with_correlation_id(correlation_id).wrap(e)

    def update(self, correlation_id, id, new_item):
        new_item = dict(new_item)
        new_item.pop('_id', None)
        new_item.pop('id', None)

        try:
            item = self._collection.find_one_and_update( \
                { '_id': id }, { '$set': new_item }, \
                return_document = pymongo.ReturnDocument.AFTER \
            )
            if self._converter != None:
                item = self._converter(item)
            return item
        except Exception as e:
            raise CallError(self, 'UpdateFailed', 'Updating item in database failed: ' + str(e)) \
                .with_correlation_id(correlation_id).wrap(e)

    # The method must return deleted value to be able to do clean up like removing references 
    def delete(self, correlation_id, id):
        try:
            item = self._collection.find_one_and_delete({ '_id': id });
            if self._converter != None:
                item = self._converter(item)
            return item
        except Exception as e:
            raise CallError(self, 'DeleteFailed', 'Deleting item in database failed: ' + str(e)) \
                .with_correlation_id(correlation_id).wrap(e)
