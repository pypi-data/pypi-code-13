# -*- coding: utf-8 -*-
import sys
import pytest
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprintpp import pprint as pp
#from dictsheet import DictSheet
#from dictsheet import  DictSheet
import dictsheet
import copy
#import test_config
import uuid 
import random
import os 

if sys.version_info.major >=3:
    import configparser as ConfigParser
    unicode = str
else:
    import ConfigParser

wks_name = unicode(uuid.uuid4())

def read_config(filename):
    config = ConfigParser.ConfigParser()
    config.readfp(open(filename))
    return config

@pytest.fixture(scope='session')
def sh():
    CONFIG_FILENAME = os.path.join(os.path.dirname(__file__), 'tests.config')
    config = read_config(CONFIG_FILENAME)
    SHEET_NAME = config.get('Settings', 'SHEET_NAME')
    CREDS_FILENAME = config.get('Settings', 'CREDENTIAL_FILE')

    scope = ['https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILENAME, scope)
    #credentials = ServiceAccountCredentials.from_json_keyfile_name('facebook-shop-cart-acdb9ee1b37e.json', scope)
    #sheet_name = u"DictSheet.test"
    sheet_name = SHEET_NAME
    gc = gspread.authorize(credentials)
    sh = gc.open(sheet_name)
    #pp(sh.worksheets())
    return sh

@pytest.fixture(scope="session")
def wks(request, sh):
    wks = sh.add_worksheet(wks_name, 20, 20)
    def wks_teardown():
        print('\nresources__teardown()')
        pp(sh.worksheets())
        print("\n %s: %s" % (wks_name, len(sh.worksheets())))
        sh.del_worksheet(wks)
        pp(sh.worksheets())
        print("\n %s: %s" % (wks_name, len(sh.worksheets())))
    request.addfinalizer(wks_teardown)
    return wks


class Test_DictSheet(object):

    @pytest.fixture(scope="session")
    def mapping(self):
        return {"key_1":1, "key_2":2, "key_3":3}

    @pytest.fixture(scope="session")
    def dict_wks(self, wks, mapping):
        dict_wks = dictsheet.DictSheet(wks=wks, mapping=mapping)
        return dict_wks

    def test_get_mapping(self, dict_wks, mapping):
        assert dict_wks.mapping == mapping
    
    def test_set_mapping(self, dict_wks, mapping):
        _mapping = copy.deepcopy(mapping)
        assert dict_wks.mapping == _mapping
        _mapping.update({"key_4": 4})
        dict_wks.mapping = _mapping
        assert dict_wks.mapping == _mapping

    def test_setter(self, dict_wks):
        with pytest.raises(IndexError):
            dict_wks[1] = {"name": "Chandler Huang",
                           "phone": "0912079235"}

        _ = {'key_1': unicode(uuid.uuid4()),
             'key_2': unicode(uuid.uuid4()),
             'key_3': unicode(uuid.uuid4()) }

        idx = random.randint(2, 10)
        for key, value in _.items():
            dict_wks[idx][key] = value
            assert value == dict_wks[idx][key]
        dict_wks[idx].clear()

    def test_update(self, dict_wks):
        _ = {'key_1': unicode(uuid.uuid4()),
             'key_2': unicode(uuid.uuid4()),
             'key_3': unicode(uuid.uuid4()) }

        idx = random.randint(2, 10)
        dict_wks[idx].update(_)
        for key, value in _.items():
            assert value == dict_wks[idx][key]
        dict_wks[idx].clear()

    
    def test_iter(self, dict_wks, wks):
        pp(dict_wks)
        pp(wks.get_all_values())
        for idx, row in enumerate(dict_wks):
            assert idx == idx
            pp(row)
    """
            if idx == 0:
                assert row['name'] == "Chandler Huang"
            if idx == 3:
                assert row['phone'] == '54321'
    """
    """
        #pp(dict_wks.__dict__['_id'])
        dict_wks.update({3: {"name": "Kelly"}, 4:{"phone": 12345}})
        assert dict_wks[3]['name'] == "Kelly"
        assert dict_wks[4]['phone'] == 12345

    def test_append(self, dict_wks):
        dict_wks.append({'name': 'TingTing', 'phone': '54321', 'address': 'no'}) 
        assert dict_wks[-1] == {'name': 'TingTing', 'phone': '54321', 'address': 'no'}
        dict_wks[-1] = {}

    def test_get(self, wks):
        #values_list = wks.row_values(1)
        #assert values_list == ""
        #assert len(values_list) == 27
        pass

    def test_entend(self):
        pass
    """

