# -*- coding: utf-8 -*-
# Copyright (c) 2016 Sqreen. All Rights Reserved.
# Please refer to our terms for more information: https://www.sqreen.io/terms.html
""" Binding accessor class
"""

import re
import types


class StringScanner(object):
    """ Equivalent of http://ruby-doc.org/stdlib-1.9.3/libdoc/strscan/rdoc/StringScanner.html
    """

    def __init__(self, string):
        self.string = string
        self.pos = 0

    def scan(self, regex):
        match = re.compile(regex).match(self.string, self.pos)

        if match:
            self.pos += len(match.group(0))
            self.match = match
            return match

    @property
    def eos(self):
        return self.pos == len(self.string)

# According to https://docs.python.org/2/reference/lexical_analysis.html#identifiers
PYTHON_IDENTIFIER = r"([a-zA-Z]|_)([a-zA-Z]|\d|_)*"


class BindingAccessor(object):
    """ Resolve the value located at the given binding
    """

    def __init__(self, expression):
        self.path = []
        self.expression = expression
        self.parse(expression)

    def __repr__(self):
        return "{}('{}')".format(self.__class__.__name__, self.expression)

    def resolve(self, binding, global_binding=None, framework=None, instance=None,
                arguments=None, kwarguments=None, cbdata=None, return_value=None):
        value = None
        env = [framework, instance, arguments, kwarguments, cbdata, return_value]

        if global_binding is None:
            global_binding = {}

        for component in self.path:
            value = self._resolve_component(value, component, binding, global_binding, env)

        self._validate_value(value)

        return value

    def _resolve_component(self, value, component, binding, global_binding, env):
        if component["kind"] in ('string', 'integer'):
            return component["value"]
        elif component["kind"] == "variable":
            return self._resolve_variable(component["name"], binding, global_binding)
        elif component["kind"] == "index":
            return value[component["index"]]
        elif component["kind"] == "attribute":
            return getattr(value, component["name"])
        elif component["kind"] == "sqreen-variable":
            return self._resolve_sqreen_variable(component["name"], *env)
        else:
            raise ValueError("Uknown component {}".format(component))

    def _resolve_sqreen_variable(self, what, framework, instance, arguments,
                                 kwarguments, cbdata, return_value):
        if what == 'data':
            return cbdata
        elif what == 'rv':
            return return_value
        elif what == 'args':
            return arguments
        elif what == 'kwargs':
            return kwarguments
        elif what == 'inst':
            return instance
        else:
            # Default to None if the framework is None
            if framework is None:
                return None

            return getattr(framework, what)

    def _resolve_variable(self, variable_name, binding, global_binding):
        if variable_name in binding:
            return binding[variable_name]
        elif variable_name in global_binding:
            return global_binding[variable_name]
        else:
            raise NameError("name '{}' was not found in bindings".format(variable_name))

    def _validate_value(self, value):
        """ In case of invalid values, raise an Exception instead
        """
        invalid_types = (types.FunctionType, types.MethodType)

        if isinstance(value, invalid_types):
            raise ValueError("Invalid return: {!r}".format(value))

    ###
    # Parse methods
    ###
    def parse(self, expression):
        self.scanner = StringScanner(expression)
        while not self.scanner.eos:
            initial_pos = self.scanner.pos

            # Check for scalar first
            scalar = self.scan_scalar()
            if scalar:
                self.path.append(scalar)
                return

            # If we are at the beginning of an expression, a variable is allowed
            if initial_pos == 0:
                self.scan_push_variable()
            else:
                self.scan_push_attribute()

            self.scan_push_indexes()

            # Remove potential dot
            self.scanner.scan(r'\.')

            if initial_pos == self.scanner.pos:
                raise ValueError('Parsing error, parser is stuck')

        # Do not keep scanner instance around
        del self.scanner

    def scan_push_variable(self):
        if self.scanner.scan(r'#\.(\w+)'):
            self.path.append({"name": self.scanner.match.group(1), "kind": "sqreen-variable"})
        elif self.scanner.scan(PYTHON_IDENTIFIER):
            self.path.append({"name": self.scanner.match.group(), "kind": "variable"})

    def scan_push_attribute(self):
        if self.scanner.scan(PYTHON_IDENTIFIER):
            self.path.append({"name": self.scanner.match.group(), "kind": "attribute"})

    def scan_scalar(self):
        if self.scanner.scan(r'\d+'):
            return {"value": int(self.scanner.match.group()), "kind": 'integer'}
        elif self.scanner.scan(r"'((?:\\.|[^\\'])*)'"):
            return {"value": self.scanner.match.group(1), "kind": 'string'}

    def scan_push_indexes(self):
        while self.scanner.scan(r"\["):
            scalar = self.scan_scalar()
            if not scalar:
                raise Exception("Invalid index")

            if not self.scanner.scan(r"\]"):
                raise ValueError("Unfinished index")

            self.path.append({"index": scalar["value"], "kind": "index"})
