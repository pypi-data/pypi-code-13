# -*- coding: utf-8 -*-
"""
    pip_services_runtime.validation.Schema
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Validation schema for complex objects.
    
    :copyright: Digital Living Software Corp. 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .PropertySchema import PropertySchema

class Schema(object):
    """
    Represents a validation schema for complex objects.
    """

    _properties = None
    _rules = None

    def __init__(self):
        """
        Creates an instance of validation schema
        """
        self._properties = []
        self._rules = []

    def get_properties(self):
        """
        Gets a list of object properties
        Returns PropertySchema list of property validation schemas
        """
        return self._properties

    def get_rules(self):
        """
        Gets a validation rules for entire object
        Returns: IValidationRule list of validation rules
        """
        return self._rules

    def with_property(self, name, type, *rules): 
        """
        Adds to the validation schema a required property defined by a simple type.
        
        Args:
            name: a name of the property to be added
            type: simple type that defines the property value
            rules: a set of validation rules for the property
            
        Returns: a self reference to the schema for chaining
        """
        self._properties.append(PropertySchema(name, False, type, False, rules))
        return self

    def with_array(self, name, type, *rules):
        """
        Adds to the validation schema a required property array defined by a simple type.
        
        Args:
            name: a name of the property to be added
            type: simple type that defines the property value
            required: a required flag
            rules: a set of validation rules for the property
        
        Returns: a self reference to the schema for chaining
        """
        self._properties.append(PropertySchema(name, True, type, False, rules))
        return self

    def with_optional_property(self, name, type, *rules):
        """
        Adds to the validation schema an optional property defined by a simple type.
        
        Args:
            name: a name of the property to be added
            type: simple type that defines the property value
            rules: a set of validation rules for the property
        
        Returns: a self reference to the schema for chaining
        """
        self._properties.append(PropertySchema(name, False, type, True, rules))
        return self

    def with_optional_array(self, name, type, *rules):
        """
        Adds to the validation schema an optional property array defined by a simple type.
        
        Args:
            name: a name of the property to be added
            type: simple type that defines the property value
            rules: a set of validation rules for the property
        
        Returns: a self reference to the schema for chaining
        """
        self._properties.append(PropertySchema(name, True, type, True, rules))
        return self

    def with_property_schema(self, name, schema, *rules):
        """
        Adds to the validation schema a required property defined by validation schema.
        
        Args:
            name: a name of the property to be added
            schema: validation schema for the property value
            required: a required flag
            rules: a set of validation rules for the property
        
        Returns: a self reference to the schema for chaining
        """
        self._properties.append(PropertySchema(name, False, schema, False, rules))
        return self

    def with_array_schema(self, name, schema, *rules):
        """
        Adds to the validation schema a required property array defined by validation schema.
        
        Args:
            name: a name of the property to be added
            schema: validation schema for the property value
            required: a required flag
            rules: a set of validation rules for the property
            
        Returns: a self reference to the schema for chaining
        """
        self._properties.append(PropertySchema(name, True, schema, False, rules))
        return self

    def with_optional_property_schema(self, name, schema, *rules):
        """
        Adds to the validation schema an optional property defined by validation schema.
        
        Args:
            name: a name of the property to be added
            schema: validation schema for the property value
            rules: a set of validation rules for the property
        
        Returns: a self reference to the schema for chaining
        """
        self._properties.append(PropertySchema(name, False, schema, True, rules))
        return self

    def with_optional_array_schema(self, name, schema, *rules):
        """
        Adds to the validation schema an optional property array defined by validation schema.
        
        Args:
            name: a name of the property to be added
            schema: validation schema for the property value
            rules: a set of validation rules for the property
        
        Returns: a self reference to the schema for chaining
        """
        self._properties.append(PropertySchema(name, True, schema, True, rules))
        return self

    def with_rule(rule):
        """
        Adds a validation rule to this scheme
        
        Args:
            rule: a validation rule to be added
        
        Returns: a self reference to the schema for chaining
        """
        self._rules.append(rule)
        return self
