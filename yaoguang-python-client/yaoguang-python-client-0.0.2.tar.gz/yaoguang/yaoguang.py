
from yaoguang.lead import Lead

from thriftpy.rpc import make_client
from thriftpy import load

import json

CONTACT=1
COMPANY=2
AD=3

class Yaoguang(object):

    def __init__(self, address):
        thrift = load("yaoguang.thrift", module_name="yaoguang_thrift")
        self._client = make_client(thrift.ThriftInterface, address, 9196)

    def bj_tags_ready(self):
        result = self._client.isReady("hello")
        json.loads(result)

    def leads(self, phone_numbers):
        asJson = self._client.get(CONTACT, [], [phone_numbers])
        return json.loads(asJson)

    def get_company(self, id):
        asJson = self._client.get(COMPANY, [], [id])
        return json.loads(asJson).get(id)

    def get_ad(self, id):
        asJson = self._client.get(AD, [], [id])
        return json.loads(asJson).get(id)
    
    def get_ads(self, ids):
        asJson = self._client.get(AD, [], ids)
        return json.loads(asJson)

    def get_contact(self, id):
        asJson = self._client.get(CONTACT, [] , [id])
        return json.loads(asJson).get(id)

    def lead(self, phone_number):
        lead = self.get_contact(phone_number)

        if lead is None:
            raise Exception('no such lead %s:' % phone_number)
            
        if 'company_id' in lead:
            id = lead['company_id']
            company = self.get_company(id)

            if 'latest_ads' in company:
                ids = list(company['latest_ads'].keys())
                ads = self.get_ads(ids)
                for key, value in ads.items():
                    company[key] = value
            lead['company'] = company

        if 'last_ad_id' in lead:
            id = lead['last_ad_id']
            lead['last_ad'] = self.get_ad(id)
        return Lead(lead)
