

from yaoguang.entity import Entities

from pygments import highlight, lexers, formatters
import json

class Lead(object):
    def __init__(self, dic):
        self._dic = dic

    def __repr__(self):
        return self._pretty()

    def __str__(self):
        return self._pretty(color=False)
        
    def _pretty(self, color=True):
        formatted_json = json.dumps(self._dic, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)
        if color:
            return highlight(formatted_json, lexers.JsonLexer(), formatters.TerminalFormatter())
        return formatted_json


class Leads(Entities):

    def get(self, phone_number):
        lead = self.get_contact(phone_number)

        if lead is None:
            raise Exception('no such lead %s:' % phone_number)
    
        return self._complete_lead(lead)

    def _complete_lead(self, lead):
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