# coding=utf-8

import importlib


def import_object(python_path):
    """Import module and object by path."""
    attribute = None

    try:
        module = importlib.import_module(python_path)
    except ImportError:
        try:
            python_path, attribute = python_path.rsplit('.', 1)
        except ValueError:
            raise ImportError(python_path)

        module = importlib.import_module(python_path)

    if attribute:
        try:
            module = getattr(module, attribute)
        except AttributeError:
            raise ImportError(python_path)

    return module
