# -*- coding: utf-8 -*-
"""
    pip_services_runtime.validation.__init__
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Data validation module initialization
    
    :copyright: Digital Living Software Corp. 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

__all__ = ['IPropertyValidationRule', 'PropertySchema', 'IValidationRule', 'Schema']

from .IPropertyValidationRule import IPropertyValidationRule
from .IValidationRule import IValidationRule
from .Schema import Schema


