#!/usr/bin/python
## 5/19/2016 - update to allow for authentication based on api-key, rather than username/pw
## See https://documentation.uts.nlm.nih.gov/rest/authentication.html for full explanation

import requests
from pyquery import PyQuery as pq
from lxml import etree

uri="https://utslogin.nlm.nih.gov"
#option 1 - username/pw authentication at /cas/v1/tickets
#auth_endpoint = "/cas/v1/tickets/"
#option 2 - api key authentication at /cas/v1/api-key
auth_endpoint = "/cas/v1/api-key"

API_KEY = "fdf782bc-2526-406d-8f78-6c632c515b48"

client = requests

class Authentication:

    m_tgt = None;

    #def __init__(self, username,password):
    def __init__(self, apikey = API_KEY):
        #self.username=username
        #self.password=password
        self.apikey=apikey
        self.service="http://umlsks.nlm.nih.gov"

    def gettgt(self):
        #params = {'username': self.username,'password': self.password}
        params = {'apikey': self.apikey}
        h = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain", "User-Agent":"python" }
        r = client.post(uri+auth_endpoint,data=params,headers=h)
        d = pq(r.text)
        ## extract the entire URL needed from the HTML form (action attribute) returned - looks similar to https://utslogin.nlm.nih.gov/cas/v1/tickets/TGT-36471-aYqNLN2rFIJPXKzxwdTNC5ZT7z3B3cTAKfSc5ndHQcUxeaDOLN-cas
        ## we make a POST call to this URL in the getst method
        tgt = d.find('form').attr('action')
        self.m_tgt = tgt;
        return tgt

    def getst(self, tgt = None):
        if tgt == None and self.m_tgt == None:
            return;
        elif tgt == None:
            tgt = self.m_tgt

        params = {'service': self.service}
        h = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain", "User-Agent":"python" }
        for retry in range(0,10):
            try:
                r = client.post(tgt,data=params,headers=h)
                if r.status_code == 200:
                    break
                else:
                    self.m_tgt = self.gettgt();
                    tgt = self.m_tgt
                    print "AUTHENTICATION FAILED, REISSUING TGT"
            except requests.exceptions.RequestException as e: 
                print "Ticket request exception happenened".upper()
                print e
                continue
        st = r.text
        #print "AUTHENTICATION SUCCESS"
        return st

def init(session = None):
    
    if session:
        print "USING SESSION"
        #client = session
    auth = Authentication(API_KEY);
    return auth


   

   
   

