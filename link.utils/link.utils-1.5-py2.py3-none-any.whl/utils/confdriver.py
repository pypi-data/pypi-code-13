# -*- coding: utf-8 -*-

from b3j0f.conf.driver.base import ConfDriver
from b3j0f.conf import Parameter

from link.feature import Feature, getfeature


class ConfigurationFeature(Feature):
    """
    Feature used to get a configuration ressource.
    """

    def get(self, rscpath):
        """
        Get configuration ressource.

        :param rscpath: Ressource's path
        :type rscpath: str

        :returns: Ressource's content
        :rtype: dict
        """

        raise NotImplementedError()


class ConfDriver(ConfDriver):
    """
    Driver that reads configuration from a feature.

    :param obj: Object providing the feature to read configuration from
    :type obj: any
    """

    def __init__(self, obj, *args, **kwargs):
        super(ConfDriver, self).__init__(*args, **kwargs)

        self.feature = getfeature(obj, 'config')

    def rscpaths(self, path):
        return [path]

    def resource(self):
        return {}

    def _pathresource(self, rscpath):
        return self.feature.get(rscpath)

    def _cnames(self, resource):
        return resource.keys()

    def _params(self, resource, cname):
        params = resource[cname]

        return [
            Parameter(name=key, svalue=params[key]) for key in params
        ]

    def _setconf(self, conf, resource, rscpath):
        for category in conf.values():
            cat = resource.setdefault(category.name, {})

            for parameter in category.values():
                cat[parameter.name] = parameter.svalue

        self.client[rscpath] = resource
