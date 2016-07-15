from unittest import TestCase
import requests_mock
from ukmdb_checkmk import ck_cmd

# http://10.20.30.40/mysite/check_mk/webapi.py?action=edit_host&_username=autouser&_secret=1122334455667788"
# -d 'request={"attributes":{"site": "testsite2"},
# "unset_attributes":["tag_criticality"], "hostname": "winxp_1"}'


class CmdEditHostTC(TestCase):

    @requests_mock.Mocker()
    def test_edit_host_01(self, my_mock):
        """ from check_mk:web/plugins/webapi/webapi.py:
        def action_edit_host(request):
            validate_request_keys(request, ["hostname", "unset_attributes", "attributes"])
        """
        my_mock.post('http://203.0.113.1/test/check_mk/webapi.py?action=edit_host',
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
        # cmd01 = cmd.GetHost(wato_url='http://203.0.113.1/test/check_mk/webapi.py',
        #                     username='auto2', password='passwd',
        #                     hostname='Hase')
        cmd01 = ck_cmd.EditHost(wato_url='http://203.0.113.1/test/check_mk/webapi.py',
                                username='auto2', password='passwd',
                                hostname='Hase',
                                attributes={'ddd': 'ddd_val'},
                                unset_attributes=['eee'])

        self.assertEqual(
            str(cmd01), "<EditHost(cmd:'EditHost(http://203.0.113.1/test/check_mk/webapi.py)', "
                        "request:'None', response:'None')>")
        self.assertEqual(cmd01.__dict__, {'wato_url': 'http://203.0.113.1/test/check_mk/webapi.py',
                                          'hostname': 'Hase', 'cmd': 'EditHost',
                                          'response': None, 'password': 'passwd',
                                          'username': 'auto2', 'request': None,
                                          'attributes': {'ddd': 'ddd_val'},
                                          'unset_attributes': ['eee']})
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
