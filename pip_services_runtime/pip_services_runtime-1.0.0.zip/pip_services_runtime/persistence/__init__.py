# -*- coding: utf-8 -*-
"""
    pip_services_runtime.persistence.__init__
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Persistence module initialization
    
    :copyright: Digital Living Software Corp. 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

__all__ = ['AbstractPersistence', 'FilePersistence', 'MemoryPersistence', 'MongoDbPersistence']

from .AbstractPersistence import AbstractPersistence
from .FilePersistence import FilePersistence
from .MemoryPersistence import MemoryPersistence
from .MongoDbPersistence import MongoDbPersistence
