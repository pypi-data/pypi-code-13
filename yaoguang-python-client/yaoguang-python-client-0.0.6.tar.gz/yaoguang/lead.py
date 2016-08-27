
from yaoguang.entity import Entities, Entity

import json


class Lead(Entity):
    pass


class Leads(Entities):

    def get(self, phone_number):
        lead = self.get_contact(phone_number)

        if lead is None:
            raise Exception('no such lead %s:' % phone_number)
    
        return self._make_lead(lead)

    def _make_lead(self, lead):
        if 'company_id' in lead:
            id = lead['company_id']
            company = self.get_company(id)

            if 'latest_ads' in company:
                ids = list(company['latest_ads'].keys())
                ads = self.get_ads(ids)
                latest_ads = {}
                for ad_id, ad in ads.items():
                    latest_ads[ad_id] = ad
                company['latest_ads'] = latest_ads

            lead['company'] = company

        if 'last_ad_id' in lead:
            id = lead['last_ad_id']
            lead['last_ad'] = self.get_ad(id)

        return Lead(lead)