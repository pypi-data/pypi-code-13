import requests
import simplejson as json

"""
document: https://developer.indiesquare.me
"""

base_url = "https://api.indiesquare.me/v2/addresses"
api_urls = { 
             'balance'    : '/balances',
             'issuance'   : '/issuances',
             'history'    : '/histories',
             }
class Address():
    def __init__(self):
        pass

    def public_base(self,url,address):
        ''' template function of public api'''
        try :
            url in api_urls
            return json.loads(requests.get(base_url + '/' + address + api_urls.get(url)).text)
        except Exception as e:
            print(e)

    def get_balance(self, address):
        return self.public_base('balance',address)
    
    def get_issuance(self, address):
        return self.public_base('issuance',address)
       
    def get_history(self, address):
        return self.public_base('history',address)
