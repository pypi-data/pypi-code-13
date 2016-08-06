# -*- coding: utf-8 -*-
"""
    pip_services_runtime.State
    ~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Component state enumeration
    
    :copyright: Digital Living Software Corp. 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class State(object):
    """
    State in lifecycle of components or the entire microservice
    """

    Undefined = -1
    """
    Undefined state
    """

    Initial = 0
    """
    Initial state right after creation
    """

    Configured = 1
    """
    Configuration was successfully completed
    """

    Linked = 2
    """
    Links between components were successfully set
    """

    Opened = 3
    """
    Ready to perform operations
    """

    Ready = 3
    """
    Ready to perform operations.
    This is a duplicate for Opened. 
    """

    Closed = 4
    """
    Closed but can be reopened
    """
