# -*- coding: utf-8 -*-
"""
    pip_services_runtime.clients.__init__
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Dependency clients module initialization
    
    :copyright: Digital Living Software Corp. 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

__all__ = ['AbstractClient', 'DirectClient', 'RestClient']

from .AbstractClient import AbstractClient
from .DirectClient import DirectClient
from .RestClient import RestClient

