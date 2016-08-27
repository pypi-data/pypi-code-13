# -*- coding: utf-8 -*-
import importlib
import logging


logger = logging.getLogger(__name__)


def load_class(fullyname):
    tokens = fullyname.split('.')
    class_name = tokens.pop()
    module_name = '.'.join(tokens)
    try:
        module = importlib.import_module(module_name)
    except ImportError as e:
        logger.error('Not able to import module named %s' % module_name)
        raise e
    try:
        ret = getattr(module, class_name)
    except AttributeError as e:
        logger.error('Not able to get class %s from module %s' %
                     (class_name, module_name))
        raise e
    return ret
