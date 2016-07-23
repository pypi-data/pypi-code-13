"""
ccli/

This module contains the source code for the ConnectWise SOAP CLI.
"""
execfile('./meta.py')

####################################################################################################
# Module Definitions

from .lib.environment import AppRcParser
ENVIRONMENT = AppRcParser()

from blessings import Terminal
TERM = Terminal()
