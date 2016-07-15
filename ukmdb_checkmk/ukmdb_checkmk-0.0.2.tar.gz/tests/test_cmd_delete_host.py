from unittest import TestCase
import requests_mock
from ukmdb_checkmk import ck_cmd

# curl
# "http://10.20.30.40/mysite/check_mk/webapi.py?action=delete_host&_username=autouser&_secret=1122334455667788"
# -d 'request={"hostname": "winxp_1"}'


class CmdDeleteHostTC(TestCase):

    @requests_mock.Mocker()
    def test_add_host_01(self, my_mock):
        """ from check_mk:web/plugins/webapi/webapi.py:
        def action_delete_host(request):
            validate_request_keys(request, ["hostname"])
        """
        my_mock.post('http://203.0.113.1/test/check_mk/webapi.py?action=delete_host',
                     json={'request': {'hostname': 'Hase'},
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
        cmd01 = ck_cmd.DeleteHost(wato_url='http://203.0.113.1/test/check_mk/webapi.py',
                                  username='auto2', password='passwd',
                                  hostname='Hase')

        self.assertEqual(
            str(cmd01), "<DeleteHost(cmd:'DeleteHost(http://203.0.113.1/test/check_mk/webapi.py)', "
                        "request:'None', response:'None')>")
        self.assertEqual(cmd01.__dict__, {'wato_url': 'http://203.0.113.1/test/check_mk/webapi.py',
                                          'hostname': 'Hase', 'cmd': 'DeleteHost',
                                          'response': None, 'password': 'passwd',
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
