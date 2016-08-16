#!/usr/bin/python3
#This is a simple library to grab an external IP.

import requests

class IPFinder:
    def __init__(self):
        self.publicip = ''
        self.privip = ''
        self.url = 'https://api.ipify.org'

    def getip(self):
        return self.publicip

    def seturl(self, url):
        self.url = url

    def updateip(self):
        try:
            r = requests.get(self.url)
            self.publicip = str(r.content, 'utf-8')
            r.close()
        except:
            self.publicip = 'ERROR'

        return self.publicip