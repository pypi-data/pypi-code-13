# -*- coding: utf-8 -*-
"""
    pip_services_runtime.data.DataPage
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Data page implementation
    
    :copyright: Digital Living Software Corp. 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class DataPage(dict):
    """
    Represents a page with optional total record counter
    """

    def __init__(self, data, total = None):
        if isinstance(data, dict):
            if 'data' in data:
                self['data'] = data['data']
            if 'total' in data:
                self['total'] = data['total']
        else:
            self['data'] = list(data)
            self['total'] = total
            