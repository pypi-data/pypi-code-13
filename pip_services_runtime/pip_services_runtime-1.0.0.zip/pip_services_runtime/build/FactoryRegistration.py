# -*- coding: utf-8 -*-
"""
    pip_services_runtime.build.FactoryRegistration
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Component factory registration record
    
    :copyright: Digital Living Software Corp. 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class FactoryRegistration(object):
    """
    Holds registration of specific component in component factory.
    """

    descriptor = None
    class_factory = None

    def __init__(self, descriptor, class_factory):
        self.descriptor = descriptor
        self.class_factory = class_factory

