from .utils import is_seq
from collections import OrderedDict

def doall(v, pipeline):
    for x in pipeline:
        v = x(v) if callable(x) else x
    return v

def render_item(description, item):
    result = OrderedDict() if isinstance(description, OrderedDict) else {}
    for key, pipeline in description.items():
        if isinstance(pipeline, dict):
            sub_description = pipeline
            result[key] = render_item(sub_description, item)
        elif isinstance(pipeline, list):
            result[key] = doall(item, pipeline)
        elif callable(pipeline):
            result[key] = pipeline(doall, item)
        else:
            raise AssertionError("render pipeline for item is an unhandled type: %r" % type(pipeline))
    return result

def render(description, data):
    assert is_seq(data), "data must be a sequence of values, not %r" % type(data)
    return map(lambda item: render_item(description, item), data)
