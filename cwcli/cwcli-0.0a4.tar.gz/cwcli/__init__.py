"""
ccli/

This module contains the source code for the ConnectWise SOAP CLI.
"""
import os


# Load the application metadata
execfile(os.path.dirname(os.path.realpath(__file__)) + '/meta.py')

####################################################################################################
# Module Definitions

from .lib.environment import AppRcParser
ENVIRONMENT = AppRcParser()

from blessings import Terminal
TERM = Terminal()
