"""
ccli/lib/transformer/json_transformer.py

This file contains the source for transforming ConnectWise objects into JSON objects.
"""
import pydash

from datetime import datetime
from collections import OrderedDict


####################################################################################################
# Classes

class JsonTransformer(object):
    """
    Generic class for transform ConnectWise objects into JSON objects.
    """

    def __init__(self):
        """
        Constructor.
        """
        pass

    def transform_to_dict(self, obj):
        """
        Transform an object into a Python dictionary.

        :param obj: Object from ConnectWise

        :return: Object as a dictionary
        """

        # If obj is None, return None
        if not obj:
            return obj

        # Create an empty dictionary to start filling with the transformed object
        obj_as_dict = OrderedDict()

        # Get all attributes on the object
        for attribute in dir(obj):

            # Ignore attributes that start with an underscore (Python standard for private
            # variables)
            if not attribute.startswith('_'):

                # Get the value of the attribute
                value = getattr(obj, attribute)

                # Check if the value is a Python type, not a ConnectWise object type
                value_check_type = pydash.partial(isinstance, value)
                if any(map(value_check_type, [
                    basestring, int, float, long, complex, bytearray, buffer, xrange, set,
                    frozenset, datetime, list, dict, tuple, bool
                ])):

                    # Convert the attribute to snake case
                    # TODO: Make this an optional flag in the CLI
                    attribute_as_snake_case = pydash.snake_case(attribute)

                    # datetime is not json serializable, so convert to string
                    if value_check_type(datetime):
                        value = value.isoformat()

                    # Add the attribute to the data dictionary
                    obj_as_dict[attribute_as_snake_case] = value

                # If the value is a function, ignore it completely
                elif callable(value):
                    continue

                # Anything that gets past the previous "if"s will be assumed to be a sub-object on
                # the ConnectWise object that should be transformed as well
                else:
                    # Convert the attribute to snake case
                    # TODO: Make this an optional flag in the CLI
                    attribute_as_snake_case = pydash.snake_case(attribute)

                    # Recursively parse the value
                    obj_as_dict[attribute_as_snake_case] = self.transform_to_dict(value)

        return obj_as_dict
