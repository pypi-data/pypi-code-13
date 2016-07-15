from unittest import TestCase
import requests_mock
from ukmdb_checkmk import ck_cmd

# self.response = requests.post("http://203.0.113.1/test/check_mk/webapi.py?action=add_host",
#                               auth=(self.username, self.password),
#                               data="request=" + json.dumps(payload))

# Example call: curl
# "http://10.20.30.40/mysite/check_mk/webapi.py?action=add_host&_username=autouser&_secret=1122334455667788"
# -d 'request={"attributes":{"alias": "Alias of winxp_1", "tag_agent":
# "cmk-agent", "tag_criticality": "prod", "ipaddress": "127.0.0.1"},
# "hostname": "winxp_1", "folder": "os/windows"}'


class CmdAddHostTC(TestCase):

    @requests_mock.Mocker()
    def test_add_host_01(self, my_mock):
        """ from check_mk:web/plugins/webapi/webapi.py:
        def action_add_host(request):
            validate_request_keys(request, ["hostname", "folder", "attributes"])
        """
        my_mock.post('http://203.0.113.1/test/check_mk/webapi.py?action=add_host',
                     json={'request': {'hostname': 'Hase',
                                       'folder': 'Tests/folder',
                                       'attributes': {'ddd': 'ddd_val'}},
                           'result': {'attributes': {'tag_srv_type': 'mail',
                                                     'tag_agent': 'ping',
                                                     'snmp_community': '',
                                                     'contactgroups': [True, ['TonD_IKOM']],
                                                     'tag_criticality': 'prod',
                                                     'alias': 'Alias of hase_dd_dd_dd_dd_dd_dd_dd_dd',
                                                     'parents': [],
                                                     'tag_location': 'loc203',
                                                     'ipaddress': '10.3.1.248',
                                                     'tag_networking': 'lan'},
                                      'hostname': 'Hase',
                                      'path': 'Tests/folder'},
                           'result_code': 0},
                     status_code=200)
        cmd01 = ck_cmd.AddHost(wato_url='http://203.0.113.1/test/check_mk/webapi.py',
                               username='auto2', password='passwd',
                               hostname='Hase',
                               folder='Tests/folder',
                               attributes={'ddd': 'ddd_val'})

        self.assertEqual(
            str(cmd01), "<AddHost(cmd:'AddHost(http://203.0.113.1/test/check_mk/webapi.py)', "
                        "request:'None', response:'None')>")
        self.assertEqual(cmd01.__dict__, {'wato_url': 'http://203.0.113.1/test/check_mk/webapi.py',
                                          'hostname': 'Hase', 'cmd': 'AddHost',
                                          'response': None, 'password': 'passwd',
                                          'folder': 'Tests/folder',
                                          'attributes': {'ddd': 'ddd_val'},
                                          'username': 'auto2', 'request': None})
        cmd01.send_request()
        self.assertEqual(cmd01.result, {'attributes': {'alias': 'Alias of hase_dd_dd_dd_dd_dd_dd_dd_dd',
                                                       'contactgroups': [True, ['TonD_IKOM']],
                                                       'ipaddress': '10.3.1.248',
                                                       'parents': [],
                                                       'snmp_community': '',
                                                       'tag_agent': 'ping',
                                                       'tag_criticality': 'prod',
                                                       'tag_location': 'loc203',
                                                       'tag_networking': 'lan',
                                                       'tag_srv_type': 'mail'},
                                        'hostname': 'Hase',
                                        'path': 'Tests/folder'})
