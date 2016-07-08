# -*- coding: utf-8 -*-
from yaml import load as yaml_load


class ApiConfiguration(object):
    """
    Configuration class for the API
    """

    def __init__(self, config_file_name='config.yaml'):
        """
        Instantiate a configuration session

        :param config_file_name: The name of the file with configuration
        :type  config_file_name: ``str``
        """
        with open(config_file_name, "r") as config_stream:
            self.config = yaml_load(config_stream)

    def providers(self):
        """
        Get a list of configured providers (driver types)

        :rtype: ``list`` of ``dict``
        """
        return [item for item in self.config['providers']]

    def clouds(self, provider):
        """
        List the configured clouds (drivers)
        for a given provider

        :rtype: ``list`` of ``dict``
        """
        return [item for item in self.config['providers'][provider]['clouds']]

    def get_cloud_args(self, provider, cloud):
        """
        Get the instance arguments for a given cloud

        :rtype: ``dict``
        """
        return self.config['configuration'][provider][cloud]

    def is_certificate_validation_enabled(self):
        """
        Is SSL certificate validation enabled

        :rtype: ``bool``
        """
        return self.config['configuration'].get(
            'disable_certificate_validation',
            False)
