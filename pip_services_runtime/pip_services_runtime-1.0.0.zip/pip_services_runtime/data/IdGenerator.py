# -*- coding: utf-8 -*-
"""
    pip_services_runtime.data.IdGenerator
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    ID generator implementation.
    
    :copyright: Digital Living Software Corp. 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import random
import uuid

class IdGenerator(object):
    """
    Generates random keys and unique ids
    """

    @staticmethod
    def short():
        return str(random.randint(100000000, 999999999))

    @staticmethod
    def uuid():
        return str(uuid.uuid4()).replace("-", "")
