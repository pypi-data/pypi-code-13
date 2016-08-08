# -*- coding: utf-8 -*-
"""
approved

:copyright: (c) 2016 by Robin Andeer
:licence: MIT, see LICENCE for more details
"""
import logging
from pkg_resources import get_distribution

__title__ = 'approved'
__summary__ = 'tool storing QC data from sequencing'
__uri__ = 'https://github.com/Clinical-Genomics/approved'

__version__ = get_distribution(__title__).version

__author__ = 'Robin Andeer'
__email__ = 'robin.andeer@scilifelab.se'

__license__ = 'MIT'
__copyright__ = 'Copyright 2015 Robin Andeer'

# the user should dictate what happens when a logging event occurs
logging.getLogger(__name__).addHandler(logging.NullHandler())
