# -*- coding: utf-8 -*-
"""
    pip_services_runtime.run.LifeCycleManager
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Component lifecycle manager implementation
    
    :copyright: Digital Living Software Corp. 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from ..State import State
from .LogWriter import LogWriter
from ..errors.UnknownError import UnknownError

class LifeCycleManager(object):
    @staticmethod
    def get_state(components):
        state = State.Undefined # Fake state

        for component in components:
            if state == State.Undefined or component.get_state() < state:
                state = component.get_state()

        return state

    @staticmethod
    def link_components(components):
        LifeCycleManager.link(ComponentSet(components))

    @staticmethod
    def link(components):
        ordered_list = components.get_all_ordered()
        for component in ordered_list:
            if component.get_state() == State.Configured:
                component.link(components)

    @staticmethod
    def link_and_open_components(components):
        LifeCycleManager.link_and_open(components)

    @staticmethod
    def link_and_open(components):
        LifeCycleManager.link(components)
        LifeCycleManager.open(components)

    @staticmethod
    def open_components(components):
        opened = []
        try:
            for component in components:
                if component.get_state() != State.Opened:
                    component.open()
                opened.append(component)
        except Exception as e:
            LogWriter.trace(components, "Microservice opening failed with error " + str(e))
            LifeCycleManager.force_close_components(opened, False)
            raise e

    @staticmethod
    def open(components):
        LifeCycleManager.open_components(components.get_all_ordered())

    @staticmethod
    def close_components(components):
        try:
            for component in reversed(components):
                if component.get_state() == State.Opened:
                    component.close()
        except Exception as e:
            LogWriter.trace(components, "Microservice closure failed with error " + str(e))
            raise e

    @staticmethod
    def close(components):
        LifeCycleManager.close_components(components.get_all_ordered())

    @staticmethod
    def force_close_components(components, throw_exception = True):
        first_error = None

        for component in reversed(components):
            try:
                if component.get_state() == State.Opened:
                    component.close()
            except MicroserviceError as e:
                LogWriter.trace(components, "Microservice closure failed with error " + str(e))
                first_error = first_error if first_error != None else e
            except Exception as e:
                LogWriter.trace(components, "Microservice closure failed with error " + str(e))
                first_error = first_error \
                    if first_error != None \
                    else UnknownError( \
                        "CloseFailed", \
                        "Failed to close component " + str(component) + ": " + str(e) \
                    ).wrap(e)

        if first_error != None and throw_exception:
            raise first_error

    @staticmethod
    def force_close(components, throw_exception = True):
        LifeCycleManager.force_close_components(components.get_all_ordered(), throw_exception)
