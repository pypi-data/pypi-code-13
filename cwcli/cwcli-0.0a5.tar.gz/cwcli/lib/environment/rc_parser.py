"""
ccli/lib/environment/rc_parser.py

This file contains the source for the ~/.*rc file parser.
"""
from __future__ import (print_function, absolute_import)

import os

from ConfigParser import ConfigParser

from cwcli import APP


####################################################################################################
# Classes

class AppRcParser(object):
    """
    Parser for the application RC file in the home directory.
    """

    def __init__(self):
        """
        Constructor.
        """
        # Check if the file exists
        self.path = '~/.{}rc'.format(APP)
        if not os.path.isfile(os.path.expanduser(self.path)):
            print('Could not find a config file at {}.'.format(self.path))
            print('Creating an empty config file. Please edit it and rerun the application.')
            self.write_empty_file()
            exit()

        # Try parsing the rc file
        self.data = {}
        self.parse()

        # Attach the configurations as attributes to this object (mostly for tooling)
        self.connectwise_site_url = self.data['connectwise_site_url']
        self.connectwise_org_name = self.data['connectwise_org_name']
        self.connectwise_username = self.data['connectwise_username']
        self.connectwise_password = self.data['connectwise_password']

    def parse(self):
        """
        Parse the RC file.

        :return: dict[str, str]
        """
        # Initialize a new instance of the config parser
        config = ConfigParser()

        # Load the file into the ConfigParser
        config.read([os.path.expanduser(self.path)])

        # Parse loaded file into key value pairs
        self.data = dict(config.items(APP))

        # Find any configurations with empty values
        empty = {k: v for k, v in self.data.items() if not v}
        if empty:
            print('The following configurations were empty: {}'.format(', '.join(empty.keys())))
            print('Please edit {} and rerun the application.'.format(self.path))
            exit()

        # If the connectiwse site url does not end with "/", append it
        if not self.data['connectwise_site_url'].endswith('/'):
            self.data['connectwise_site_url'] += '/'

    def write_empty_file(self):
        """
        Write the RC file with empty values.

        :return: None
        """
        # Initialize a new instance of the config parser
        config = ConfigParser()

        # Add the section for the app
        config.add_section(APP)

        # Add the configurations with empty values
        config.set(APP, 'CONNECTWISE_PASSWORD', '')
        config.set(APP, 'CONNECTWISE_USERNAME', '')
        config.set(APP, 'CONNECTWISE_SITE_URL', '')
        config.set(APP, 'CONNECTWISE_ORG_NAME', '')

        # Write the fields to the RC file
        config.write(open(os.path.expanduser(self.path), 'w'))
