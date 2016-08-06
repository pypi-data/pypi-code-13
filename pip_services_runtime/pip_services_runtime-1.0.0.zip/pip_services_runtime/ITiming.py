# -*- coding: utf-8 -*-
"""
    pip_services_runtime.ITiming
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Callback interface to complete measuring time interval.
    
    :copyright: Digital Living Software Corp. 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class ITiming(object):
    """
    Callback interface to complete measuring time interval
    """

    def end_timing(self):
        """
        Completes measuring time interval and updates counter.

        Returns: None
        """
        #raise NotImplementedError('Method from interface definition')
        pass
