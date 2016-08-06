# -*- coding: utf-8 -*-
"""
    pip_services_runtime.validation.PropertySchema
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Validation schema for object properties
    
    :copyright: Digital Living Software Corp. 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

#from .Schema import Schema
import Schema

class PropertySchema(object):
    """
    Represents a validation schema for object property.
    The schema can use simple types like: "string", "number", "object", "DummyObject"
    or specific schemas for object values
    """

    _name = ""
    _array = False
    _optional = False
    _type = "any"
    _schema = None
    _rules = None

    def __init__(self, name, array, type_or_schema, optional = False, rules = None):
        """
        Creates instance of the object property schema defined by a simple type
        
        Args: 
            name: the name of the property
            array: the array flag
            type_or_schema: the simple value type as string or Schema object
            optional: the optional flag
            rules: IPropertyValidationRule list of validation rules
        """

        self._name = name
        self._array = array
        self._optional = optional
        self._rules = []
        
        if isinstance(type_or_schema, Schema.Schema):
            self._schema = type_or_schema
        else:
            self._type = type_or_schema
        
        if type(rules) == tuple: 
            rules = list(rules)
        self._rules = rules or []

    def get_name(self):
        """
        Gets the property name
        Returns: the name of the property
        """
        return self._name
 
    def is_array(self):
        """
        Gets the property array flag
        Returns: True if the property is array and False if it is a simple value
        """
        return self._array

    def is_optional(self):
        """
        Gets the property optional flag (opposite to required)
        @return True if the property optional and False if it is required
        """
        return self._optional

    def get_type(self):
        """
        Gets the simple type describing property value
        Returns: a simple value type: 'int', 'float', 'number', 'string', 'boolean', 'string', ...
        """
        return self._type

    def get_schema(self):
        """
        Gets the complex property schema describing property value
        Returns: a schema object
        """
        return self._schema

    def get_rules(self):
        """
        Gets a list of validation rules associated with this property
        Returns: IPropertyValidationRule list of validation rules
        """
        return self._rules
