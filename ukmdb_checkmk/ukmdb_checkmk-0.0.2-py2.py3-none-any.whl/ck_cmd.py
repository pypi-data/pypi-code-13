"""
Class for WatoCmd
"""
# pylint: disable=R0903,W0201

import logging
import json
import requests

UKMDB_LOG = logging.getLogger("ukmdb")


class WatoCmd(object):
    """
    commands for Wato web-api from check_mk
    """

    def __init__(self, wato_url, username, password):
        self.wato_url = wato_url
        self.username = username
        self.password = password
        self.request = None
        self.response = None
        self.cmd = type(self).__name__

    def __repr__(self):
        return '<' + \
            type(self).__name__ + \
            "(cmd:'%(cmd)s(%(wato_url)s)', request:'%(request)s', response:'%(response)s')" % self.__dict__ + \
            '>'


class AddHost(WatoCmd):
    """
    With the action add_host you can add a new host to WATO.

    An example request payload for a new host may look like::

        {
            "attributes": {
                "tag_criticality": "prod",
                "tag_agent": "cmk-agent",
                "alias": "Alias of winxp_1",
                "ipaddress": "127.0.0.1",
            },
            "folder":   "os/windows",
            "hostname": "winxp_1"
        }

    You need to specify the hostname and the folder where the host resides.
    Additionally, you may add further elements into the attributes dictionary.
    In the attributes block you can set values like alias and ipaddress and
    even host tags. Host tags are specified by tag_{groupname} : value Per
    default, non-existing host folders are created automatically. You can
    change this behaviour with the additional parameter create_folders=0.

    Example call::

        curl "http://10.20.30.40/mysite/check_mk/webapi.py?action=ad
        d_host&_username=autouser&_secret=mysecret" -d
        'request={"attributes":{"alias": "Alias of winxp_1", "tag_agent": "cmk-
        agent", "tag_criticality": "prod", "ipaddress": "127.0.0.1"}, "hostname":
        "winxp_1", "folder": "os/windows"}'
    """

    def __init__(self, wato_url, username, password,
                 folder, hostname, attributes=None):
        super().__init__(wato_url, username, password)
        if attributes is None:
            attributes = {}
        self.folder = folder
        self.hostname = hostname
        self.attributes = attributes
        UKMDB_LOG.debug("""WatoCmd:add_host_Cmd(
            wato_url='%(wato_url)s',
            username='%(username)s',
            folder='%(folder)s',
            hostname='%(hostname)s',
            attrib='%(attrib)s'
            )""", self.__dict__)

    def send_request(self):
        """This function translates foo into bar

        :param foo: A string to be converted
        :returns: A bar formatted string
        """
        UKMDB_LOG.debug("WatoCmd:add_host_Cmd.send_request()")
        payload = {'hostname': self.hostname,
                   'folder': self.folder,
                   'attributes': self.attributes}
        self.response = requests.post("%s?action=add_host" % self.wato_url +
                                      "&_username=%s" % self.username +
                                      "&_secret=%s" % self.password,
                                      auth=(self.username, self.password),
                                      data="request=" + json.dumps(payload))
        self.request = self.response.request
        self.result = self.response.json()['result']
        self.resultcode = self.response.json()['result_code']
        UKMDB_LOG.debug("url: %s", self.response.url)
        UKMDB_LOG.debug("request body: %s", self.response.request.body)
        UKMDB_LOG.info("return text: %s", self.response.text)
        UKMDB_LOG.info("return status_code: %s", self.response.status_code)
        UKMDB_LOG.info("reason: %s", self.response.reason)
        if self.resultcode != 0:
            raise Exception(self.response.text)
        return self.result


class EditHost(WatoCmd):
    """
    With the action edit_host you can edit an already existing WATO host. You
    can only change a hosts attributes, but NOT the hosts folder.

    An example request payload for a new host may look like::

        {
            "attributes": {
                "site": "testsite2"
            },
            "unset_attributes": ["tag_criticality"],
            "hostname": "winxp_1"
        }

    Since the hostname is unique within WATO you only need to specify the host
    via the hostname parameter. You are able to update the attributes with new
    values. Further attributes of this host, which are not mentioned in the
    attributes block are not modified. Furthermore, via unset_attributes you
    can unset attributes for this host, so they are no longer explicitly set
    and can be inherited from parent folders.

    Example call::

        curl "http://10.20.30.40/mysite/check_mk/webapi.py?action=ed
        it_host&_username=autouser&_secret=mysecret" -d
        'request={"attributes":{"site": "testsite2"},
        "unset_attributes":["tag_criticality"], "hostname": "winxp_1"}'
    """

    def __init__(self, wato_url, username, password,
                 hostname, attributes=None, unset_attributes=None):
        super().__init__(wato_url, username, password)
        if attributes is None:
            attributes = {}
        if unset_attributes is None:
            unset_attributes = []
        self.hostname = hostname
        self.attributes = attributes
        self.unset_attributes = unset_attributes
        UKMDB_LOG.debug("""WatoCmd:edit_host_Cmd(
            wato_url='%(wato_url)s',
            username='%(username)s',
            hostname='%(hostname)s',
            attributes='%(attributes)s',
            unset_attributes='%(unset_attributes)s',
            )""", self.__dict__)

    def send_request(self):
        UKMDB_LOG.debug("WatoCmd:edit_host_Cmd.send_request()")
        payload = {'hostname': self.hostname,
                   'attributes': self.attributes,
                   'unset_attributes': self.unset_attributes}
        self.response = requests.post("%s?action=edit_host" % self.wato_url +
                                      "&_username=%s" % self.username +
                                      "&_secret=%s" % self.password,
                                      auth=(self.username, self.password),
                                      data="request=" + json.dumps(payload))
        self.request = self.response.request
        self.result = self.response.json()['result']
        self.resultcode = self.response.json()['result_code']
        UKMDB_LOG.debug("url: %s", self.response.url)
        UKMDB_LOG.debug("request body: %s", self.response.request.body)
        UKMDB_LOG.debug("return text: %s", self.response.text)
#        wato_logger.info("return text / result_code: %s" % self.response.text['result_code'])
        UKMDB_LOG.debug("return status_code: %s", self.response.status_code)
        UKMDB_LOG.debug("reason: %s", self.response.reason)
        if self.resultcode != 0:
            raise Exception(self.response.text)
        return self.result


class DeleteHost(WatoCmd):
    """
    With the action delete_host you can delete a host in WATO.

    An example request payload for a new host may look like::

        { "hostname": "winxp_1" }

    Example call: curl "http://10.20.30.40/mysite/check_mk/webapi.py?action=de
    lete_host&_username=autouser&_secret=mysecret" -d 'request={"hostname":
    "winxp_1"}'
    """

    def __init__(self, wato_url, username, password, hostname):
        super().__init__(wato_url, username, password)
        self.hostname = hostname
        UKMDB_LOG.debug("""cmd.DeleteHost(
            wato_url='%(wato_url)s',
            username='%(username)s',
            hostname='%(hostname)s',
            )""", self.__dict__)

    def send_request(self):
        UKMDB_LOG.debug("cmd.DeleteHost.send_request()")
        payload = {'hostname': self.hostname}
        self.response = requests.post("%s?action=delete_host" % self.wato_url +
                                      "&_username=%s" % self.username +
                                      "&_secret=%s" % self.password,
                                      auth=(self.username, self.password),
                                      data="request=" + json.dumps(payload))
        self.request = self.response.request
        self.result = self.response.json()['result']
        self.resultcode = self.response.json()['result_code']
        UKMDB_LOG.debug("url: %s", self.response.url)
        UKMDB_LOG.debug("request body: %s", self.response.request.body)
        UKMDB_LOG.info("return text: %s", self.response.text)
        UKMDB_LOG.info("return status_code: %s", self.response.status_code)
        UKMDB_LOG.info("reason: %s", self.response.reason)
        if self.resultcode != 0:
            raise Exception(self.response.text)
        return self.result


class GetHost(WatoCmd):
    """

    With the get_host action you can query the attributes of the given host.

    An example request payload for a new host may look like::

    { "hostname": "winxp_1" }

    This request returns only the explicitly set attributes of this host. If
    you want to have also the inherited attributes from the parent folders you
    need to add the parameter effective_attributes=1.

    Example call::

        curl "http://10.20.30.40/mysite/check_mk/webapi.py?action=ge
        t_host&_username=autouser&_secret=mysecret&effective_attributes=1" -d
        'request={"hostname": "winxp_1"}'

    """

    def __init__(self, wato_url, username, password,
                 hostname):
        super().__init__(wato_url, username, password)
        self.hostname = hostname
        UKMDB_LOG.debug("""WatoCmd:get_host_Cmd(
            wato_url='%(wato_url)s',
            username='%(username)s',
            hostname='%(hostname)s',
            )""", self.__dict__)

    def send_request(self):
        UKMDB_LOG.debug("WatoCmd:get_host_Cmd.send_request()")
        payload = {'hostname': self.hostname}
        self.response = requests.post("%s" % self.wato_url +
                                      "?action=get_host" +
                                      "&_username=%s" % self.username +
                                      "&_secret=%s" % self.password +
                                      "&effective_attributes=1",
                                      auth=(self.username, self.password),
                                      data="request=" + json.dumps(payload))
        UKMDB_LOG.debug("response: %s", self.response)
        UKMDB_LOG.debug("response.json(): %s", self.response.json())
        self.request = self.response.request
        self.result = self.response.json()['result']
        self.resultcode = self.response.json()['result_code']
        UKMDB_LOG.debug("url: %s", self.response.url)
        UKMDB_LOG.debug("request body: %s", self.response.request.body)
        UKMDB_LOG.info("return text: %s", self.response.text)
        UKMDB_LOG.info("return status_code: %s", self.response.status_code)
        UKMDB_LOG.info("reason: %s", self.response.reason)
        if self.resultcode != 0:
            raise Exception(self.response.text)
        return self.result


class GetAllHosts(WatoCmd):
    """
    With the get_all_hosts action you can query the attributes of all hosts
    managed in WATO.

    The default request returns only the explicitly set attributes of the
    hosts. If you want to have also the inherited attributes from the parent
    folders you need to add the parameter effective_attributes=1.

    Example call::

        curl "http://10.20.30.40/mysite/check_mk/webapi.py?action=ge
        t_all_hosts&_username=autouser&_secret=mysecret&effective_attributes=1"
    """

    def __init__(self, wato_url, username, password):
        super().__init__(wato_url, username, password)
        UKMDB_LOG.debug("""WatoCmd:get_all_host_Cmd(
            wato_url='%(wato_url)s',
            username='%(username)s',
            )""", self.__dict__)

    def send_request(self):
        UKMDB_LOG.debug("WatoCmd:get_all_host_Cmd.send_request()")
        payload = {}
        self.response = requests.post("%s" % self.wato_url +
                                      "?action=get_all_hosts" +
                                      "&_username=%s" % self.username +
                                      "&_secret=%s" % self.password +
                                      "&effective_attributes=1",
                                      auth=(self.username, self.password),
                                      data="request=" + json.dumps(payload))
        UKMDB_LOG.debug("response: %s", self.response)
        UKMDB_LOG.debug("response.json(): %s", self.response.json())
        self.request = self.response.request
        self.result = self.response.json()['result']
        self.resultcode = self.response.json()['result_code']
        UKMDB_LOG.debug("url: %s", self.response.url)
        UKMDB_LOG.debug("request body: %s", self.response.request.body)
        UKMDB_LOG.info("return text: %s", self.response.text)
        UKMDB_LOG.info("return status_code: %s", self.response.status_code)
        UKMDB_LOG.info("reason: %s", self.response.reason)
        if self.resultcode != 0:
            raise Exception(self.response.text)
        return self.result


class DiscoverServices(WatoCmd):
    """
    With the discover_services action you can start a service inventory for
    the given host.

    An example request payload for a new host may look like::

        { "hostname": "winxp_1" }

    Per default, the inventory only tries to find new services. You can
    configure this behaviour with the additional parameter mode which can have
    the following options:

    new
        Only find new services (default)
    remove
        Remove exceeding services
    fixall
        Remove exceeding and add new services
    refresh
        Clean all autochecks and start from scratch - Tabula Rasa

    Example call::

        curl "http://10.20.30.40/mysite/check_mk/webapi.py?action=di
        scover_services&_username=autouser&_secret=mysecret&mode=refresh" -d
        'request={"hostname": "winxp_1"}'
    """

    def __init__(self, wato_url, username, password, hostname, mode='new'):
        super().__init__(wato_url, username, password)
        self.hostname = hostname
        self.mode = mode
        UKMDB_LOG.debug("""cmd.DiscoverServices(
            wato_url='%(wato_url)s',
            username='%(username)s',
            hostname='%(hostname)s',
            mode='%(mode)s',
            )""", self.__dict__)

    def send_request(self):
        UKMDB_LOG.debug("cmd.DiscoverServices.send_request()")
        payload = {'hostname': self.hostname}
        self.response = requests.post("%s?action=discover_services&mode=%s" %
                                      (self.wato_url, self.mode) +
                                      "&_username=%s" % self.username +
                                      "&_secret=%s" % self.password,
                                      auth=(self.username, self.password),
                                      data="request=" + json.dumps(payload))
        self.request = self.response.request
        self.result = self.response.json()['result']
        self.resultcode = self.response.json()['result_code']
        UKMDB_LOG.debug("url: %s", self.response.url)
        UKMDB_LOG.debug("request body: %s", self.response.request.body)
        UKMDB_LOG.info("return text: %s", self.response.text)
        UKMDB_LOG.info("return status_code: %s", self.response.status_code)
        UKMDB_LOG.info("reason: %s", self.response.reason)
        if self.resultcode != 0:
            raise Exception(self.response.text)
        return self.result


class ActivateChanges(WatoCmd):
    """
    With the activate_changes action you can basically do the same as you've
    pressed the Activate changes! button in the Web-GUI. If applicable, the
    changed configuration will be deployed on the slave sites, followed by a
    monitoring core reload. Unlike the GUI version, this API action can not
    update multiple slave sites in parallel. Instead it contacts one after
    another, sends the new configuration and wait till the core has reloaded.
    This could lead to (apache timeout) problems in environments with multiple
    slave sites.

    An example request payload for a new host may look like::

        { "sites": ["site_nr1", "site_nr2"] }

    The sites key is optional.

    You can restrict which sites to update with the parameter mode, which can
    have the following options:

    dirty    Only update sites with changes (default)
    all    Updates all slave sites
    specific    Only updates sites specified in the request parameter

    You can also set the parameter allow_foreign_changes=1 to take over
    changes from foreign users. If this parameter is not set and a foreign
    user has made changes, the request will fail.

    Example call::

        curl "http://10.20.30.40/mysite/check_mk/webapi.py?action=ac
        tivate_changes&_username=autouser&_secret=mysecret&mode=specific" -d
        'request={"sites":["site_nr1", "site_nr2"]}'
    """

    def __init__(self, wato_url, username, password, sites=None, mode='dirty', allow_foreign_changes=False):
        super().__init__(wato_url, username, password)
        self.sites = sites
        self.mode = mode
        self.allow_foreign_changes = allow_foreign_changes
        UKMDB_LOG.debug("""WatoCmd:activate_changes_Cmd(
            wato_url='%(wato_url)s',
            username='%(username)s',
            sites='%(sites)s',
            mode='%(mode)s',
            allow_foreign_changes='%(allow_foreign_changes)s',
            )""", self.__dict__)

    def send_request(self):
        UKMDB_LOG.debug("WatoCmd:activate_changes_Cmd.send_request()")
        payload = {}
        self.response = requests.post("%s?action=activate_changes&mode=dirty" % self.wato_url +
                                      "&_username=%s" % self.username +
                                      "&_secret=%s" % self.password,
                                      auth=(self.username, self.password),
                                      data="request=" + json.dumps(payload))
        self.request = self.response.request
        self.result = self.response.json()['result']
        self.resultcode = self.response.json()['result_code']
        UKMDB_LOG.debug("url: %s", self.response.url)
        UKMDB_LOG.debug("request body: %s", self.response.request.body)
        UKMDB_LOG.info("return text: %s", self.response.text)
        UKMDB_LOG.info("return status_code: %s", self.response.status_code)
        UKMDB_LOG.info("reason: %s", self.response.reason)
        if self.resultcode != 0:
            raise Exception(self.response.text)
        return self.result
