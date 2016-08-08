"""Generate commands to import mongodb schema to a RDBMS.

This module allows for command line or programtic generation RDBMS schemas
from a json-like format.
-Ryan Birmingham
"""
import json


class SchemaConv(object):
    """An object to keep track of and manage schema conversion.

    Args:
        jsonin: A string, file, or file path containing a json representation.
    """

    def __init__(self, jsonin):
        """initalize, trying to normalize input."""
        if type(jsonin) is str:
            self.jsonin = jsonin
        else:
            if type(jsonin) is not file:
                try:
                    jsonin = open(jsonin)
                except IOError:
                    raise IOError('Input file interpreted as path,'
                                  'not found')
                except TypeError:
                    raise TypeError('input type not understood')
            self.jsonin = jsonin.read().splitlines()
        self.jsonin = json.loads(self.jsonin)
        raise FutureWarning("SchemaConv under construction.")

    def __str__(self):
        """Return a string for command line invoke."""
        return "SchemaConv instance."
