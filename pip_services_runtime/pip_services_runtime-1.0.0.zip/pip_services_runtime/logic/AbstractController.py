# -*- coding: utf-8 -*-
"""
    pip_services_runtime.logic.AbstractController
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Abstract business logic controller implementation
    
    :copyright: Digital Living Software Corp. 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .AbstractBusinessLogic import AbstractBusinessLogic

class AbstractController(AbstractBusinessLogic):
    """
    Abstract implementation for business logic controller.
    """

    def __init__(self, descriptor):
        """
        Creates instance of abstract controller
        
        Args:
            descriptor: the unique descriptor that is used to identify and locate the component.
        """
        super(AbstractController, self).__init__(descriptor)

    def link(self, components):
        """
        Sets references to other microservice components to enable their 
        collaboration. It is recommended to locate necessary components
        and cache their references to void performance hit during normal operations. 

        Linking can only be performed once after configuration 
        and will cause an exception when it is called second time or out of order.

        Args: 
            components: references to microservice components.

        Returns: None
        
        Raises:
            MicroserviceError: when requires components are not found.
        """
        super(AbstractController, self).link(components)
        
        # Commented until we decide to use command pattern as everywhere
        # Until now the main method is to implement specific methods with instrumentation
        #self._add_intercepter(TracingIntercepter(self._loggers, "Executing"))
        #self._add_intercepter(TimingIntercepter(self._counters, "exec_time"))

    def _instrument(self, correlation_id, name):
        """
        Does instrumentation of performed business method by counting elapsed time.
        
        Args:
            correlation_id: the unique id to identify distributed transaction
            name: the name of called business method
        
        Returns: ITiming instance to be called at the end of execution of the method.
        """
        self.trace(None, "Executing " + name + " method")
        return self.begin_timing(name + ".exec_time")
