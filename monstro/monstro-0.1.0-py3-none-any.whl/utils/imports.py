# coding=utf-8

import importlib


def import_object(python_path):
    """Import module and object by path."""
    paths = python_path.split('.')
    count = len(paths)
    index = 0
    module = None

    while index < count:
        try:
            module = importlib.import_module('.'.join(paths[:count-index]))
            break
        except ImportError:
            index += 1

    if module is None:
        raise ImportError(python_path)

    if index:
        for key in paths[-index:]:
            try:
                module = getattr(module, key)
            except AttributeError:
                raise ImportError(python_path)

    return module
