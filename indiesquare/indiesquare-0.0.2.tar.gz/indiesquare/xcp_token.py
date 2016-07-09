import requests
import simplejson as json

"""
document: https://developer.indiesquare.me
"""

base_url = "https://api.indiesquare.me/v2/tokens"
api_urls = { 
             'search'    : '?name=',
             'get_token'   : '',
             }
class Token():
    def __init__(self):
        pass

    def public_base(self,url,_token):
        ''' template function of public api'''
        try :
            url in api_urls
            print(base_url + api_urls.get(url) + _token)
            return json.loads(requests.get(base_url + api_urls.get(url) + _token).text)
        except Exception as e:
            print(e)

    def search_token(self, _token):
        return self.public_base('search',_token)
    
    def get_token(self, _token):
        return self.public_base('get_token',_token)
