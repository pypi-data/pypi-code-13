# -*- coding: utf-8 -*-
"""
    pip_services_runtime.data.FilterParams
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Free-form filter parameters implementation
    
    :copyright: Digital Living Software Corp. 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from ..portability.DynamicMap import DynamicMap

class FilterParams(DynamicMap):
    """
    Stores free-form parameters as key-value pairs
    """

    def __init__(self, map = None):
        if map != None:
            for (key, value) in map.items():
                self[key] = value

    @staticmethod
    def from_value(value):
        if isinstance(value, FilterParams):
            return value
        if isinstance(value, DynamicMap):
            return FilterParams(value)
        
        return FilterParams(DynamicMap.from_value(value))

    @staticmethod
    def from_tuples(*tuples):
        filter = FilterParams()
        filter.set_tuples_array(tuples)
        return filter

    @staticmethod
    def from_map(map):
        return FilterParams(map)
