import json
from namespaces import FrozenNamespace, Namespace

class NamespaceEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, FrozenNamespace):
      return obj._dict
    elif isinstance(obj, Namespace):
      return obj # rely on dict inheritance
    return json.JSONEncoder.default(self, obj)

