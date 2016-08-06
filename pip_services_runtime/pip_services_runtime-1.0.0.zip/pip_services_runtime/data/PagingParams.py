# -*- coding: utf-8 -*-
"""
    pip_services_runtime.data.PagingParams
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Data paging parameters implementation
    
    :copyright: Digital Living Software Corp. 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from ..portability.Converter import Converter
from ..portability.DynamicMap import DynamicMap

class PagingParams(dict):
    """
    Stores data paging parameters
    """

    def __init__(self, skip = None, take = None, total = True):
        self['skip'] = Converter.to_nullable_integer(skip)
        self['take'] = Converter.to_nullable_integer(take)
        self['total'] = Converter.to_boolean_with_default(total, True)

    def get_skip(self, min_skip):
        if self['skip'] == None:
            return min_skip
        if self['skip'] < min_skip:
            return min_skip
        return self['skip'] 

    def get_take(self, max_take):
        if self['take'] == None:
            return max_take
        if self['take'] < 0:
            return 0
        if self['take'] > max_take:
            return max_take
        return self['take'] 

    def is_total(self):
        return self['total']

    @staticmethod
    def from_value(value):
        if isinstance(value, PagingParams):
            return value
        if isinstance(value, DynamicMap):
            return PagingParams.from_map(value)
        
        map = DynamicMap.from_value(value)
        return PagingParams.from_map(map)

    @staticmethod
    def from_tuples(*tuples):
        map = DynamicMap()
        map.set_tuples_array(tuples)
        return PagingParams.from_map(map)

    @staticmethod
    def from_map(map):
        skip = map.get_nullable_integer("skip")
        take = map.get_nullable_integer("take")
        total = map.get_nullable_boolean("total")
        return PagingParams(skip, take, total)
