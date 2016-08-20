#######################################################################
# Loads configuration files written in Python.
#
# Copyright 2011-2016 True Blade Systems, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Notes:
#  There are obviously security implications with running arbitrary
# python scripts as your config files. Only use in appropriate
# situations.
########################################################################

import os
import collections

__all__ = ['loads', 'load', 'SimpleFileLoader']

_DEFAULT_NAMESPACE = 'Namespace'

def loads(s, globals=None, locals=None, name='<string>', namespace_name=None):
    if globals is None:
        globals = {}
    if locals is None:
        locals = {}
    if namespace_name is None:
        namespace_name = _DEFAULT_NAMESPACE

    # call compile() so that errors have a decent context
    code = compile(s, name, 'exec')
    exec(code, globals, locals)

    # convert to a namedtuple so we have easy access to the fields
    fields = sorted([name for name in locals.keys() if not name.startswith('_')])
    result_type = collections.namedtuple(namespace_name, fields)

    # and instantate the result with our values
    return result_type(*[locals[name] for name in result_type._fields])


def load(fl, globals=None, locals=None, name=None, namespace_name=None):
    """Load from a file-like object. It is the caller's responsibility to close the file."""
    return loads(fl.read(), globals, locals, name, namespace_name)


class SimpleFileLoader(object):
    '''A simple loader that reads from local files, and has an include() function to load additional files.'''

    def __init__(self, dirname, include_fn_name='include', builtins=None, other_globals=None):
        self.dirname = dirname
        self.globals = {}
        self.locals = {}

        if builtins is not None:
            self.globals['__builtins__'] = builtins

        if other_globals is not None:
            self.globals.update(other_globals)

        if include_fn_name is not None:
            self.globals[include_fn_name] = self.__call__

    def __call__(self, filename):
        with open(os.path.join(self.dirname, filename)) as fl:
            return load(fl, globals=self.globals, locals=self.locals, name=filename)


