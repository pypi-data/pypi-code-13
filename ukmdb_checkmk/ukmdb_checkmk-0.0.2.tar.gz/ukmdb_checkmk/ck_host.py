# pylint: disable=E1101
"""
.. module:: app01.models2
   :platform: Unix, Windows
   :synopsis: A useful module indeed.

.. moduleauthor:: Markus Leist

checkmk host object
"""
# pylint: disable=W0612,W1401

import re
import logging
from cachetools.func import ttl_cache
from ukmdb_checkmk import ck_cmd

WATO_LOGGER = logging.getLogger('wato_cmds')
WATO_LOGGER.debug(u"Debugging wato_cmd with level: 'DEBUG'")


class CheckMkHost(object):
    """ CheckMkHost is a special class for configuration of objects in
    the check_mk-application
    """

    def __init__(self, context, folder, hostname):
        """This method creates an check_mk host object with

        :param context: Value 1.
        :type context: int.
        :param folder: Value 2.
        :type folder: int.
        :param hostname: Value 2.
        :type hostname: int.
        :returns:  None.

        """
        self.context = context
        self.__folder = folder
        self.__hostname = hostname
        WATO_LOGGER.debug("CheckMkHost.__init__(%s, %s)", folder, hostname)
        ecmd = ck_cmd.GetHost(wato_url=self.context['wato_url'],
                              username=self.context['username'],
                              password=self.context['password'],
                              hostname=self.hostname)
        result = ecmd.send_request()
        self.request = ecmd.request
        self.response = ecmd.response
        self.__attributes = result['attributes']
        self.__hostname = result['hostname']
        self.__path = result['path']

    def get_folder(self):
        return self.__folder

    def get_hostname(self):
        return self.__hostname

    def get_attributes(self):
        WATO_LOGGER.debug("CheckMkHost.get_attributes()")
        ecmd = ck_cmd.GetHost(wato_url=self.context['wato_url'],
                              username=self.context['username'],
                              password=self.context['password'],
                              hostname=self.hostname)
        result = ecmd.send_request()
        self.request = ecmd.request
        self.response = ecmd.response
        self.__attributes = result['attributes']
        return self.__attributes

    @property
    @ttl_cache(ttl=3)
    def attributes(self):
        WATO_LOGGER.debug("CheckMkHost.attributes()  111")
        ecmd = ck_cmd.GetHost(wato_url=self.context['wato_url'],
                              username=self.context['username'],
                              password=self.context['password'],
                              hostname=self.hostname)
        result = ecmd.send_request()
        self.request = ecmd.request
        self.response = ecmd.response
        self.__attributes = result['attributes']
        return self.__attributes

    @attributes.setter
    def attributes(self, value):
        WATO_LOGGER.debug("CheckMkHost.attributes()  222")
        self.__attributes = value

    @attributes.deleter
    def del_attributes(self):
        del self.__attributes

    def set_folder(self, value):
        self.__folder = value

    def set_hostname(self, value):
        """This function does a * b.

        :param val01: Value 1.
        :type val01: int.
        :param val02: Value 2.
        :type val02: int.
        :returns:  int -- val01 * val02.

        >>> my_function(2, 3)
        6
        >>> my_function('a', 3)
        'aaaa'
        """
        self.__hostname = value

    def set_attributes(self, value):
        WATO_LOGGER.debug("CheckMkHost.set_attributes()")
        self.__attributes = value

    def del_folder(self):
        del self.__folder

    def del_hostname(self):
        del self.__hostname

    @property
    def ip_address(self):
        "IP address getter"
        WATO_LOGGER.debug("CheckMkHost.ip_address() getter")
        return self.attributes['ipaddress']

    @ip_address.setter
    def ip_address(self, value):
        "IP address setter"
        WATO_LOGGER.debug("CheckMkHost.ip_address() setter")
        ecmd = ck_cmd.EditHost(wato_url=self.context['wato_url'],
                               username=self.context['username'],
                               password=self.context['password'],
                               hostname=self.hostname,
                               attributes={'ipaddress': value})
        ecmd.send_request()
        self.request = ecmd.request
        self.response = ecmd.response

    @ip_address.deleter
    def ip_address(self):
        "IP address deleter"
        WATO_LOGGER.debug("CheckMkHost.ip_address() deleter")
        ecmd = ck_cmd.EditHost(wato_url=self.context['wato_url'],
                               username=self.context['username'],
                               password=self.context['password'],
                               hostname=self.hostname,
                               unset_attributes=['ipaddress'])
        ecmd.send_request()
        self.request = ecmd.request
        self.response = ecmd.response

    @property
    def alias(self):
        WATO_LOGGER.debug("CheckMkHost.alias() getter")
        return self.attributes['alias']

    @alias.setter
    def alias(self, value):
        WATO_LOGGER.debug("CheckMkHost.alias() setter")
        ecmd = ck_cmd.EditHost(wato_url=self.context['wato_url'],
                               username=self.context['username'],
                               password=self.context['password'],
                               hostname=self.hostname,
                               attributes={'alias': value})
        ecmd.send_request()
        self.request = ecmd.request
        self.response = ecmd.response

    @alias.deleter
    def alias(self):
        WATO_LOGGER.debug("CheckMkHost.alias() deleter")
        ecmd = ck_cmd.EditHost(wato_url=self.context['wato_url'],
                               username=self.context['username'],
                               password=self.context['password'],
                               hostname=self.hostname,
                               unset_attributes=['alias'])
        ecmd.send_request()
        self.request = ecmd.request
        self.response = ecmd.response

    def get_tags(self):
        WATO_LOGGER.debug("CheckMkHost.get_tags()")
        all_tags = {}
        for attr in self.attributes:
            parsed = re.match('^tag_(\w+)', attr)
            if parsed:
                all_tags[parsed.group(1)] = self.attributes[attr]
        return all_tags

    def set_tag(self, key, value):
        WATO_LOGGER.debug("CheckMkHost.set_tag('%s','%s')", key, value)
        ecmd = ck_cmd.EditHost(wato_url=self.context['wato_url'],
                               username=self.context['username'],
                               password=self.context['password'],
                               hostname=self.hostname,
                               attributes={'tag_' + key: value})
        result = ecmd.send_request()  # noqa
        self.request = ecmd.request
        self.response = ecmd.response

    folder = property(get_folder, set_folder, del_folder, "folder's docstring")
    hostname = property(get_hostname, set_hostname,
                        del_hostname, "hostname's docstring")

    def commit(self):
        """This function does a * b.

        :param val01: Value 1.
        :type val01: int.
        :param val02: Value 2.
        :type val02: int.
        :returns:  int -- val01 * val02.
        """
        WATO_LOGGER.debug("CheckMkHost.commit()")
        ecmd = ck_cmd.ActivateChanges(wato_url=self.context['wato_url'],
                                      username=self.context['username'],
                                      password=self.context['password'])
        result = ecmd.send_request()  # noqa
        self.request = ecmd.request
        self.response = ecmd.response

    def rollback(self):
        WATO_LOGGER.debug("CheckMkHost.rollback()")
