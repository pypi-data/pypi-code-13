from __future__ import absolute_import, unicode_literals
import json
from namespaces import FrozenNamespace, Namespace

class NamespaceEncoder(json.JSONEncoder):
  '''Custom JSON encoder that converts both FrozenNamespace and Namespace to a dict.'''
  def default(self, obj):
    if isinstance(obj, FrozenNamespace) or isinstance(obj, Namespace):
      return dict(obj)
    return json.JSONEncoder.default(self, obj)

