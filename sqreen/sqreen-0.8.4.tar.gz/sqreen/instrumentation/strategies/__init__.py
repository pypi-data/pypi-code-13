# -*- coding: utf-8 -*-
# Copyright (c) 2016 Sqreen. All Rights Reserved.
# Please refer to our terms for more information: https://www.sqreen.io/terms.html
""" Hijacking strategies
"""
import sys
import logging

from importlib import import_module

from ..helpers import partial
from ..hook_point import hook_point, DjangoMiddleware
from ..import_hook import ImportHook, get_hook_parent, get_hook_path
from ...exceptions import SqreenException

from .base import BaseStrategy
from .dbapi2 import DBApi2Strategy
from .import_hook import ImportHookStrategy
from .psycopg2 import Psycopg2Strategy

LOGGER = logging.getLogger(__name__)


class InvalidHookPoint(SqreenException):
    """ Exception raised when the hook_point couldn't be found or is invalid
    """
    pass


class SetAttrStrategy(BaseStrategy):
    """ Simple strategy that calls setattr(hook_module, hook_name, callback)
    """

    def __init__(self, hook_name, channel, before_hook_point=None):
        super(SetAttrStrategy, self).__init__(channel, before_hook_point)
        self.hook_module, self.hook_name = hook_name
        self.original = self._get_original()

    def hook(self, callback):
        """ Accept a callback and store it. If it's the first callback
        for this strategy, actually hook to the endpoint.
        """
        self.add_callback(callback)

        # Check that we didn't already hooked the endpoint
        if self.hooked is False:
            _hook_point = partial(hook_point, self, callback.hook_module,
                                  callback.hook_name, self.original)

            module = self._get_hook_to()
            setattr(module, self.hook_name, _hook_point)

            self.hooked = True

    def _get_original(self):
        """ Return the original function defined at (hook_module, hook_name)
        """

        if self.hook_name == '':
            raise InvalidHookPoint('Empty hook_name')

        module = self._get_hook_to()

        try:
            return getattr(module, self.hook_name)
        except AttributeError:
            msg = "Bad hook_name {} on hook_module {}"
            raise InvalidHookPoint(msg.format(self.hook_name,
                                              self.hook_module))

    def _get_hook_to(self):
        """ Retrieve the python module or class corresponding to hook_name
        """

        if self.hook_module == '':
            raise InvalidHookPoint('Empty hook_module')

        # Check if the klass is part module and part klass name
        if '::' in self.hook_module:
            module_name, class_name = self.hook_module.split('::', 1)
        else:
            module_name, class_name = self.hook_module, None

        try:
            module = import_module(module_name)
        except ImportError:
            raise InvalidHookPoint("Bad module name {}".format(module_name))

        if class_name:
            try:
                module = getattr(module, class_name)
            except AttributeError:
                msg = "Bad class_name {} on module {}".format(class_name, module_name)
                raise InvalidHookPoint(msg)

        return module

    @staticmethod
    def get_strategy_id(callback):
        """ Return the tuple (callback.hook_module, callback.hook_name) as
        identifier for this strategy
        """
        return (callback.hook_module, callback.hook_name)

    def _restore(self):
        """ Restore the original function at the hooked path
        """
        module = self._get_hook_to()
        setattr(module, self.hook_name, self.original)
        self.hooked = False


###
# Django
###


def load_middleware_insert(original, middleware):

    def wrapped_load_middleware(self, *args, **kwargs):
        LOGGER.debug("Execute load_middleware_insert")

        # Load original middlewares
        result = original(self, *args, **kwargs)

        # Insert out custom one
        try:
            self._view_middleware.insert(0, middleware.process_view)
            self._response_middleware.append(middleware.process_response)
            self._exception_middleware.append(middleware.process_exception)
        except Exception:
            LOGGER.warning("Error while inserting our middleware", exc_info=True)

        return result

    return wrapped_load_middleware


class DjangoStrategy(BaseStrategy):
    """ Strategy for Django peripheric callbacks.

    It injects a custom DjangoFramework that calls callbacks for each
    lifecycle method
    """

    MODULE_NAME = "django.core.handlers.base"
    HOOK_CLASS = "BaseHandler"
    HOOK_METHOD = "load_middleware"

    def __init__(self, strategy_key, channel, before_hook_point=None):
        super(DjangoStrategy, self).__init__(channel, before_hook_point)
        self.strategy_key = strategy_key

        self.django_middleware = DjangoMiddleware(self, channel)

        self.hooked = False

    def hook(self, callback):
        """ Accept a callback and store it. If it's the first callback
        for this strategy, actually hook the load_middleware to insert our
        middleware.

        Once hooked, the middleware will call the callbacks at the right moment.
        """
        # Register callback
        self.add_callback(callback)

        # Check if we already hooked at
        if not self.hooked:

            import_hook = ImportHook(self.MODULE_NAME, self.import_hook_callback)
            sys.meta_path.insert(0, import_hook)

            self.hooked = True

    def import_hook_callback(self, module):
        """ Monkey-patch the object located at hook_class.hook_name on an
        already loaded module
        """
        hook_parent = get_hook_parent(module, self.HOOK_CLASS)

        original = getattr(hook_parent, self.HOOK_METHOD, None)
        hooked = load_middleware_insert(original, self.django_middleware)
        setattr(hook_parent, self.HOOK_METHOD, hooked)
        LOGGER.debug("Successfully hooked on %s %s", self.MODULE_NAME,
                     self.HOOK_CLASS)

    @classmethod
    def get_strategy_id(cls, callback):
        """ This strategy only hook on
        (django.core.handlers.base::BaseHandler, load_middleware)
        """
        return ("{}::{}".format(cls.MODULE_NAME, cls.HOOK_CLASS), cls.HOOK_METHOD)

    def _restore(self):
        """ The hooked module will always stay hooked
        """
        pass
