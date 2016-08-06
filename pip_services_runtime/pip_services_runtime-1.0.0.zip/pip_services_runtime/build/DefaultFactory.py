# -*- coding: utf-8 -*-
"""
    pip_services_runtime.build.DefaultFactory
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Default component factory implementation
    
    :copyright: Digital Living Software Corp. 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .ComponentFactory import ComponentFactory
from ..logs.NullLogger import NullLogger
from ..logs.ConsoleLogger import ConsoleLogger
from ..counters.NullCounters import NullCounters
from ..counters.LogCounters import LogCounters
from ..cache.NullCache import NullCache
from ..cache.MemoryCache import MemoryCache
from ..boot.FileBootConfig import FileBootConfig

class DefaultFactory(ComponentFactory):
    """
    Component factory that contains registrations of standard runtime components.
    This factory is typically used as a base for microservice factories.
    """

    def __init__(self):
        """
        Creates an instance of default factory with standard runtime components 
        """
        super(DefaultFactory, self).__init__()

        self.register(NullLogger.Descriptor, NullLogger)
        self.register(ConsoleLogger.Descriptor, ConsoleLogger)
        self.register(NullCounters.Descriptor, NullCounters)
        self.register(LogCounters.Descriptor, LogCounters)
        self.register(NullCache.Descriptor, NullCache)
        self.register(MemoryCache.Descriptor, MemoryCache)
        self.register(FileBootConfig.Descriptor, FileBootConfig)
        
DefaultFactory.Instance = DefaultFactory()
"""
The instance of default factory
"""
