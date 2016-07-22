# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Helper functions for deconstructing classes, functions, and user-defined
objects into serializable types.
"""

from types import FunctionType, BuiltinFunctionType

from .primtive_types import return_primitive


def class_from_serializable_representation(class_repr):
    """
    Given the name of a module and a class it contains, imports that module
    and gets the class object from it.
    """
    module_string, class_name = class_repr
    module_parts = module_string.split(".")
    attribute_list = module_parts[1:] + class_name.split(".")
    # traverse the chain of imports and nested classes to get to the
    # actual class value
    value = __import__(module_parts[0])
    for name in attribute_list:
        value = getattr(value, name)
    return value

def class_to_serializable_representation(cls):
    """
    Given a class, return two strings:
        - fully qualified import path for its module
        - name of the class

    The class can be reconstructed from these two strings by calling
    class_from_serializable_representation.
    """
    return (cls.__module__, cls.__name__)

@return_primitive
def function_from_serializable_representation(fn_repr):
    """
    Given the name of a module and a function it contains, imports that module
    and gets the class object from it.
    """
    module_string, class_name = fn_repr
    module = __import__(module_string)
    return getattr(module, class_name)


@return_primitive
def function_to_serializable_representation(fn):
    """
    Converts a Python function into a serializable representation. Does not
    currently work for methods or functions with closure data.
    """
    if type(fn) not in (FunctionType, BuiltinFunctionType):
        raise ValueError(
            "Can't serialize %s : %s, must be globally defined function" % (
                fn, type(fn),))

    if hasattr(fn, "__closure__") and fn.__closure__ is not None:
        raise ValueError("No serializable representation for closure %s" % (fn,))

    return (fn.__module__, fn.__name__)

@return_primitive
def object_to_serializable_representation(obj):
    """
    Given an instance of a Python object, returns a tuple whose
    first element is a primitive representation of the class and whose
    second element is a dictionary of instance data.
    """
    if not hasattr(obj, 'to_dict'):
        raise ValueError("Expected %s to have method to_dict()" % (obj,))

    state_dict = obj.to_dict()
    class_representation = class_to_serializable_representation(obj.__class__)
    return (class_representation, state_dict)


@return_primitive
def object_from_serializable_representation(obj_repr):
    """
    Given a primitive representation of some object, reconstructs
    the class from its module and class names and then instantiates. Returns
    instance object.
    """
    class_repr, state_dict = obj_repr
    subclass = class_from_serializable_representation(class_repr)
    return subclass.from_dict(state_dict)
