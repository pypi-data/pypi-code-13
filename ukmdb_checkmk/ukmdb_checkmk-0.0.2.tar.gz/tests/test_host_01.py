from unittest import TestCase
import requests_mock
from ukmdb_checkmk import ck_host


@requests_mock.Mocker()
class WatoHost01TC(TestCase):

    def test_host_01_01(self, my_mock):
        # mock for get host
        my_mock.register_uri('POST',
                             'http://203.0.113.1/test/check_mk/webapi.py?action=get_host&effective_attributes=1',
                             json={'request': {'hostname': 'Hase'},
                                   'result': {'attributes': {'tag_srv_type': 'mail',
                                                             'tag_agent': 'ping',
                                                             'snmp_community': '',
                                                             'contactgroups': [True, ['TonD_IKOM']],
                                                             'tag_criticality': 'prod',
                                                             'alias': 'Alias of hase',
                                                             'parents': [],
                                                             'tag_location': 'loc203',
                                                             'ipaddress': '10.3.1.248',
                                                             'tag_networking': 'lan'},
                                              'hostname': 'Hase',
                                              'path': 'Tests/folder'},
                                   'result_code': 0},
                             status_code=200)
        # mock for edit host
        my_mock.register_uri('POST',
                             'http://203.0.113.1/test/check_mk/webapi.py?action=edit_host',
                             json={'request': {'hostname': 'Hase'},
                                   'result': {'attributes': {'tag_srv_type': 'mail',
                                                             'tag_agent': 'ping',
                                                             'snmp_community': '',
                                                             'contactgroups': [True, ['TonD_IKOM']],
                                                             'tag_criticality': 'prod',
                                                             'alias': 'Alias of hase',
                                                             'parents': [],
                                                             'tag_location': 'loc203',
                                                             'ipaddress': '10.3.1.248',
                                                             'tag_networking': 'lan'},
                                              'hostname': 'Hase',
                                              'path': 'Tests/folder'},
                                   'result_code': 0},
                             status_code=200)

        # mock for activate_changes
        my_mock.register_uri('POST',
                             'http://203.0.113.1/test/check_mk/webapi.py?action=activate_changes&mode=dirty',
                             json={'request': {'hostname': 'Hase'},
                                   'result': {'attributes': {'tag_srv_type': 'mail',
                                                             'tag_agent': 'ping',
                                                             'snmp_community': '',
                                                             'contactgroups': [True, ['TonD_IKOM']],
                                                             'tag_criticality': 'prod',
                                                             'alias': 'Alias of hase',
                                                             'parents': [],
                                                             'tag_location': 'loc203',
                                                             'ipaddress': '10.3.1.248',
                                                             'tag_networking': 'lan'},
                                              'hostname': 'Hase',
                                              'path': 'Tests/folder'},
                                   'result_code': 0},
                             status_code=200)

        const_context = {'wato_url': 'http://203.0.113.1/test/check_mk/webapi.py',
                         'username': 'username',
                         'password': 'password'}
        c_mk_host01 = ck_host.CheckMkHost(
            context=const_context, folder='Tests', hostname='Hase')
        c_mk_host01.alias += '_dd'

        c_mk_host01.commit()
        self.assertEqual(str(c_mk_host01.response), "<Response [200]>")
