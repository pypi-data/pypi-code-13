# -*- coding: utf-8 -*-
"""
    pip_services_runtime.portability.DynamicMap
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Portable implementation of dynamic map object
    
    :copyright: Digital Living Software Corp. 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .Converter import Converter

class DynamicMap(dict):
    """
    Portable implementation of dynamic data object represented as hash-map of values.
    It supports handling hierarchical data structures and arrays
    """
    
    def __init__(self, map = None):
        """
        Constructs and initiatizes the instance of dynamic map

        Args:
            map: (options) a hashmap with values
        """
        if isinstance(map, dict):
            for (k, v) in map.items():
                self[k] = v

    ############## Getters ##############

    def get(self, path):
        if path == None or path == '': 
            return None
        
        props = path.split(".")
        container = self

        for prop in props:
            if not isinstance(container, dict):
                return None
            
            if not (prop in container):
                return None

            container = container[prop]

        return container

    def has(self, path):
        return self.get(path) != None

    def has_not(self, path):
        return self.get(path) == None

    def get_nullable_map(self, path):
        value = self.get(path)
        return Converter.to_nullable_map(value)

    def get_map(self, path):
        value = self.get(path)
        map = Converter.to_nullable_map(value)
        return map if map != None else DynamicMap()

    def get_map_with_default(self, path, default_value):
        value = self.get(path)
        return Converter.to_map_with_default(value, default_value)

    def get_nullable_array(self, path):
        value = self.get(path)
        
        # Return None when nothing found
        if value == None:
            return None
        # Convert list
        elif type(value) in (list, tuple, set):
            return list(value)
        # Convert single values
        else:
            return [value]

    def get_array(self, path):
        value = self.get_nullable_array(path)
        return value if value != None else []

    def get_array_with_default(self, path, default_value):
        value = self.get_nullable_array(path)
        return value if value != None else default_value

    def get_nullable_string(self, path):
        value = self.get(path)
        return Converter.to_nullable_string(value)

    def get_string(self, path):
        return self.get_string_with_default(path, "")

    def get_string_with_default(self, path, default_value):
        value = self.get(path)
        return Converter.to_string_with_default(value, default_value)

    def get_nullable_boolean(self, path):
        value = self.get(path)
        return Converter.to_nullable_boolean(value)

    def get_boolean(self, path):
        return self.get_boolean_with_default(path, False)

    def get_boolean_with_default(self, path, default_value):
        value = self.get(path)
        return Converter.to_boolean_with_default(value, default_value)

    def get_nullable_integer(self, path):
        value = self.get(path)
        return Converter.to_nullable_integer(value)

    def get_integer(self, path):
        return self.get_integer_with_default(path, 0)

    def get_integer_with_default(self, path, default_value):
        value = self.get(path)
        return Converter.to_integer_with_default(value, default_value)

    def get_nullable_long(self, path):
        value = self.get(path)
        return Converter.to_nullable_long(value)

    def get_long(self, path):
        return self.get_long_with_default(path, 0L)

    def get_long_with_default(self, path, default_value):
        value = self.get(path)
        return Converter.to_long_with_default(value, default_value)

    def get_nullable_float(self, path):
        value = self.get(path)
        return Converter.to_nullable_float(value)

    def get_float(self, path):
        return get_float_with_default(path, 0.0)
        
    def get_float_with_default(self, path, default_value):
        value = self.get(path)
        return Converter.to_float_with_default(value, default_value)

    def get_nullable_date(self, path):
        value = self.get(path)
        return Converter.to_nullable_date(value)

    def get_date(self, path):
        return self.get_date_with_default(path, None)
        
    def get_date_with_default(self, path, default_value):
        value = get(path)
        return Converter.to_date_with_default(value, default_value)

    ########### Setters ###############

    def set(self, path, value):
        if path == None or path == '':
            return

        props = path.split(".")
        if len(props) == 0:
            return
        
        container = self

        for prop in props[:-1]:
            if not (prop in container):
                temp = DynamicMap()
                container[prop] = temp
                container = temp
            else:
                prop_value = container[prop]
                if not isinstance(prop_value, dict):
                    return                
                container = prop_value
        
        container[props[-1]] = value

    def set_tuples_array(self, values):
        i = 0 
        while i < len(values) - 1:
            path = Converter.to_string(values[i])
            value = values[i + 1]
            
            self.set(path, value)
            i = i + 2

    def set_tuples(self, *values):
        self.set_tuples_array(values)

    def remove(self, prop):
        # Todo: implement hierarchical delete
        self.pop(prop, None)

    def remove_all(self, *props):
        for prop in props:
            self.remove(prop)

    ############# Merging ###############

    @staticmethod
    def _merge(dest, source, deep):
        if dest == None:
            dest = DynamicMap()
        if source == None:
            return dest

        for (key, value) in source.items():
            if key in dest:
                dest_value = dest[key]
                default_value = value

                if deep and isinstance(dest_value, dict) and isinstance(default_value, dict):
                    value = DynamicMap._merge(dest_value, default_value, deep)
                    dest[key] = value
            else:
                dest[key] = value

        return dest

    @staticmethod
    def merge(dest, source, deep):
        return DynamicMap._merge(dest, source, deep)

    def merge(self, source, deep):
        dest = DynamicMap(self)
        return DynamicMap._merge(dest, source, deep)

    def merge_deep(self, source):    	
        return self.merge(source, True)

    ################ Other Utilities ##############

    def assign_to(self, value):
        if value == None:
            return

        if type(value) == dict:
            for (prop, prop_value) in self.items():
                value[prop] = prop_value
        else:
            for (prop, prop_value) in self.items():
                if hasattr(value, prop):
                    setattr(value, prop, prop_value)

    def pick(self, *props):
        result = DynamicMap()

        for prop in props:
            if prop in self:
                value = self[prop]
                result[prop] = value

        return result

    def omit(self, *props):
        result = DynamicMap(self)        

        for prop in props:
            result.remove(prop)

        return result
 
    ########### Class constructors #############

    @staticmethod
    def from_value(value):
        """
        Creates a dynamic map from free-form object by converting it into the map.

        Args:
            value: a free-form object

        Returns: a constructed DynamicMap
        """
        return Converter.to_map(value)

    @staticmethod
    def from_tuples(*tuples):
        """
        Creates a dynamic map from list of <path> + <value> tuples

        Args:
            tuples: tuples that contain property path following with property value

        Returns: a constructed dynamic map
        """
        result = DynamicMap()
        result.set_tuples_array(tuples)
        return result
