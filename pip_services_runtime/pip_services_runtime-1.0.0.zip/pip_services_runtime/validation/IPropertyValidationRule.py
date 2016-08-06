# -*- coding: utf-8 -*-
"""
    pip_services_runtime.validation.IPropertyValidationRule
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for property validation rules.
    
    :copyright: Digital Living Software Corp. 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class IPropertyValidationRule(object):
    """
    Interface for object property validation rule.
    If can performs validation for a specified object property.
    For instance, it check for valid range, allowed or disallowed values.
    """

    def validate(self, schema, value):
        """
        Validates object property according to the schema and the rule.
        
        Args:
            schema: a property schema this rule belongs to
            value: the property value to be validated.
        
        Returns: MicroserviceError list with validation errors or empty list if validation passed.
        """
        raise NotImplementedError('Method from interface definition')