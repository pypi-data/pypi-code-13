# -*- coding: utf-8 -*-
"""
    pip_services_runtime.portability.Converter
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Data conversion utilities
    
    :copyright: Digital Living Software Corp. 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from datetime import *
import json
import iso8601
import pytz
import DynamicMap

class Converter(object):

    @staticmethod
    def to_nullable_string(value):
        # Shortcuts
        if value == None:
            return None        
        return str(value)

    @staticmethod
    def to_string(value):
        return Converter.to_string_with_default(value, '')

    @staticmethod
    def to_string_with_default(value, default_value):
        result = Converter.to_nullable_string(value)
        return result if result != None else default_value
        
    @staticmethod
    def to_nullable_boolean(value):
        # Shortcuts
        if value == None:
            return None
        if type(value) == type(True):
            return value

        str_value = str(value).lower()
        # All true values
        if str_value in ['1', 'true', 't', 'yes', 'y']:
            return True
        # All false values
        if str_value in ['0', 'frue', 'f', 'no', 'n']:
            return False

        # Everything else:
        return None

    @staticmethod
    def to_boolean(value):
        return Converter.to_boolean_with_default(value, False)

    @staticmethod
    def to_boolean_with_default(value, default_value):
        result = Converter.to_nullable_boolean(value)
        return result if result != None else default_value

    @staticmethod
    def to_nullable_long(value):
        # Shortcuts
        if value == None:
            return None

        try:
            value = float(value)
            return long(value)
        except:
            return None

    @staticmethod
    def to_long(value):
        return Converter.to_long_with_default(value, 0L)

    @staticmethod
    def to_long_with_default(value, default_value):
        result = Converter.to_nullable_long(value)
        return result if result != None else default_value

    @staticmethod
    def to_nullable_integer(value):
        # Shortcuts
        if value == None:
            return None

        try:
            value = float(value)
            return int(value)
        except:
            return None

    @staticmethod
    def to_integer(value):
        return Converter.to_integer_with_default(value, 0)

    @staticmethod
    def to_integer_with_default(value, default_value):
        result = Converter.to_nullable_integer(value)
        return result if result != None else default_value

    @staticmethod
    def to_nullable_float(value):
        # Shortcuts
        if value == None:
            return None

        try:
            return float(value)
        except:
            return None

    @staticmethod
    def to_float(value):
        return Converter.to_float_with_default(value, 0.0)

    @staticmethod
    def to_float_with_default(value, default_value):
        result = Converter.to_nullable_float(value)
        return result if result != None else default_value

    @staticmethod
    def to_nullable_date(value):
        # Shortcuts
        if value == None:
            return None
        if type(value) == datetime:
            return value 

        if type(value) in (int, float, long):
            return datetime.fromtimestamp(value)
        if type(value) == date:
            return datetime.combine(value, time(0,0,0))
        if type(value) == time:
            return datetime.combine(datetime.utcnow().date, value)
        
        try:
            value = str(value)
            return iso8601.parse_date(value)
        except:
            return None

    @staticmethod
    def to_date(value):
        return Converter.to_date_with_default(value, None)

    @staticmethod
    def to_date_with_default(value, default_value):
        result = Converter.to_nullable_date(value)
        return result if result != None else default_value

    @staticmethod
    def to_nullable_array(value):
        # Shortcuts
        if value == None:
            return None
        if type(value) == list:
            return value 

        if type(value) in [tuple, set]:
            return list(value)
            
        return [value]

    @staticmethod
    def to_array(value):
        return Converter.to_array_with_default(value, [])

    @staticmethod
    def to_array_with_default(value, default_value):
        result = Converter.to_nullable_array(value)
        return result if result != None else default_value

    @staticmethod
    def list_to_array(value):
        if value == None:
            return []
        elif type(value) in [list, tuple, set]:
            return list(value)
        elif type(value) in [str, unicode]:
            return value.split(',')
        else:
            return [value]

    @staticmethod
    def from_multi_string(value, language = 'en'):
        if value == None or (type(value) in [str, unicode]):
            return value

        result = getattr(value, language)
        if result != None and result != '': 
            return result

        result = getattr(value, 'en')
        if result != None and result != '': 
            return result
        
        for prop in dir(value):
            result = getattr(value, prop)
            if result != None and result != '': 
                return result
        
        return None

    @staticmethod
    def _value_to_map(value, classkey = None):
        if isinstance(value, dict):
            data = DynamicMap.DynamicMap()
            for (k, v) in value.items():
                data[k] = Converter._value_to_map(v, classkey)
            return data
        elif hasattr(value, "_ast"):
            return Converter._value_to_map(value._ast())
        elif hasattr(value, "__iter__"):
            return [Converter._value_to_map(v, classkey) for v in value]
        elif hasattr(value, "__dict__"):
            data = dict([(key, Converter._value_to_map(value, classkey)) 
                for key, value in value.__dict__.iteritems() 
                if not callable(value) and not key.startswith('_')])
            if classkey is not None and hasattr(value, "__class__"):
                data[classkey] = value.__class__.__name__
            return DynamicMap.DynamicMap(data)
        else:
            return value

    @staticmethod
    def to_nullable_map(value):
        if value == None:
            return None

        # Parse JSON
        if type(value) in [str, unicode]:
            try:
                value = json.loads(value)
            except:
                return None
        
        # Default parsing
        result = Converter._value_to_map(value)
        if isinstance(result, DynamicMap.DynamicMap):
            return result
        return None

    @staticmethod
    def to_map(value):
        result = Converter.to_nullable_map(value)
        return result if result != None else DynamicMap.DynamicMap()

    @staticmethod
    def to_map_with_default(value, default_value):
        result = Converter.to_nullable_map(value)
        return result if result != None else default_value
