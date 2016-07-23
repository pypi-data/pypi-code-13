"""
ccli/lib/connectwise/common.py

Common classes that will be used by all API modules in this module.
"""
import logging
import sys

from suds.client import Client
from suds import WebFault

from cwcli import ENVIRONMENT, TERM


####################################################################################################
# Setup Logging

logging.basicConfig(level=logging.ERROR, filename='suds.log')
logging.getLogger('suds.client').setLevel(logging.ERROR)


####################################################################################################
# Custom Errors

class ConnectwiseApiError(Exception):
    """
    Base class for encountered ConnectWise API errors.
    """
    pass


####################################################################################################
# Classes

class ConnectwiseApi(object):
    """
    Base class for creating a ConnectWise API.
    """

    def __init__(self, wsdl_name):
        """
        Constructor.

        :param wsdl_name: Name of the .wsdl file for this API.
        :type wsdl_name: str
        """
        # Initialize the suds client
        self.client = Client('{}v4_6_release/apis/2.0/{}?wsdl'.format(ENVIRONMENT.connectwise_site_url, wsdl_name))

        # Initialize the suds credentials object
        self.credentials = self.client.factory.create('ApiCredentials')
        self.credentials.CompanyId = ENVIRONMENT.connectwise_org_name
        self.credentials.IntegratorLoginId = ENVIRONMENT.connectwise_username
        self.credentials.IntegratorPassword = ENVIRONMENT.connectwise_password

    @staticmethod
    def handle_errors(func):
        """
        Try to run the passed function and catch any common ConnectWise errors.

        :param func: Function which makes a request to ConnectWise.

        :return: Wrapped function.
        """

        # Create a wrapped function
        def wrapped(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except WebFault as e:
                if 'First error message' in e.message:
                    e.message = e.message.split('First error message: ')[1][:-1]
                print('{t.bright_red}{e.message}{t.normal}'.format(t=TERM, e=e))
                sys.exit()

        return wrapped
