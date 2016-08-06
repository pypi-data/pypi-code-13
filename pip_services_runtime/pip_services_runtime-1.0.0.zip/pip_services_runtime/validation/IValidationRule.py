# -*- coding: utf-8 -*-
"""
    pip_services_runtime.validation.IValidationRule
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for schema validation rules.
    
    :copyright: Digital Living Software Corp. 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class IValidationRule(object):
    """
    Interface for object schema validation rule.
    If can performs overall validation across the entire object.
    For instance, it can check presence of one of several required properties.
    """

    def validate(self, schema, value):
        """
        Validates object according to the schema and the rule.
        
        Args:
            schema: an object schema this rule belongs to
            value: the object value to be validated.
        
        Returns: MicroserviceError list with validation errors or empty list if validation passed.
        """
        raise NotImplementedError('Method from interface definition')