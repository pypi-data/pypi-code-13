'''
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
'''

from umls_auth import Authentication
import requests
import grequests
import signal
import sys
import time
import json
import pickle
import shelve 
import copy

def pretty_print(data):
	print json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))

DEFAULT_CACHE = "umls_cache"
MAX_LENGTH = 1000000

pageSize = 400

class RequestManager:
	m_auth = None
	m_cache = None
	m_service="http://umlsks.nlm.nih.gov"
	m_session = requests.Session()



	def __init__(self, cache_path = None):
		self.m_auth = Authentication()
		self.m_TGT = self.m_auth.gettgt()
		signal.signal(signal.SIGINT, self.signal_handler)
		self.load_cache()
		self.sync_counter = 0
		if cache_path:
			DEFAULT_CACHE = cache_path


	def cache_response(self, url, resp):
		if self.m_cache != None and resp.status_code == 200:
			try:
				self.m_cache[url] = resp
			except Exception, e:
				print str(e)
				return

			while len(self.m_request_list) > MAX_LENGTH:
				print "EVICTING REQUEST FROM CACHE"
				del self.m_cache[self.m_request_list[-1]]
				self.m_request_list.pop()

			self.m_request_list.append(url)
			print "CACHE SIZE: " + str(len(self.m_request_list))
			self.sync_counter = self.sync_counter + 1
			if self.sync_counter > 10:
				print "SYNCING CACHE"
				self.reload_cache()
				#self.m_cache.sync()
				self.sync_counter = 0


	def request_exception_handler(self, request, exception):
		print "Request failed: "
		print request
		print exception


	def auth_exception_handler(self, request, exception):
		print "Auth failed: "
		print request
		print exception


	def async_request(self, i, url, ticket):
		if ticket and ticket.text:
			ticket = ticket.text
		else:
			ticket = ""
		print "Generating request for url: " + url + " using ticket " + ticket
		payload = {'ticket': ticket, 'pageSize': pageSize};
		return grequests.get(url, params = payload, session = self.m_session)


	def async_auth(self, i, window_size):
		print "Generating ticket " + str(i) + ", " + str(window_size) + " needed"
		params = {'service': self.m_service}
		h = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain", "User-Agent":"python"}
		return grequests.post(self.m_TGT,data=params,headers=h, session = self.m_session)


	def pipeline_get(self, urls, **args):
		responses = range(0, len(urls))

		urls_in_cache = {}
		urls_not_in_cache = {}

		for url_idx in range(0, len(urls)):
			url = str(urls[url_idx])
			if self.m_cache and url in self.m_cache:
				print "Url already in cache: " + url 
				urls_in_cache[url] = url_idx
				responses[url_idx] = self.m_cache[url]
			else:
				urls_not_in_cache[url] = url_idx

		urls_to_get = urls_not_in_cache.keys()
		num_requests = len(urls_to_get)

		auth_post_list = (self.async_auth(i, num_requests) for i in range(0, num_requests))
		tickets = grequests.map(auth_post_list, self.request_exception_handler)
		ticket_tups = ({
			"idx": i, 
			"url": urls_to_get[i],
			"ticket": tickets[i]
		} for i in range(0, num_requests))
		request_list = (self.async_request(tup["idx"], tup["url"], tup["ticket"]) for tup in ticket_tups)
		new_responses = grequests.map(request_list, self.auth_exception_handler)

		for resp_idx in range(0, num_requests):
			self.cache_response(urls_to_get[resp_idx], new_responses[resp_idx])
			responses[urls_not_in_cache[urls_to_get[resp_idx]]] = new_responses[resp_idx]

		'''
		for url in urls:
			responses.append(self.single_get(url, **copy.deepcopy(args)))
		'''

		return responses


	def single_get(self, url, **args):
		url = str(url)

		print args

		if self.m_cache != None and url in self.m_cache:
			#print "CACHE HIT"
			return self.m_cache[url]

		if 'params' not in args:
			args['params'] = {}

		if 'ticket' not in args['params']:
			args["params"]["ticket"] = self.m_auth.getst()
			print args["params"]["ticket"]
		
		for retry in range(0, 10):
			try:
				resp = requests.get(url, **args)
				if resp.status_code == 200:
					break;
				else:
					print "request failed for " + url 
			except requests.exceptions.RequestException as e: 
				print e
				continue

		return resp


	def get(self, urls, **args):
		if isinstance(urls, list):
			print "PIPELINING"
			#print urls
			return self.pipeline_get(urls, **args)
		else:
			print "SINGLE REQUEST"
			return self.single_get(urls, **args)


	def signal_handler(self, signal, frame):
		print 'Writing cache to disk'
		self.write_cache()
		sys.exit(0)


	def load_cache(self, path = DEFAULT_CACHE):
		#self.m_cache = shelve.open(path, writeback = True)
		try:
			self.m_cache = shelve.open(path, writeback = True)
			if "request_list" in self.m_cache:
				self.m_request_list = self.m_cache["request_list"]
			else:
				self.m_request_list = []
				self.m_cache["request_list"] = self.m_request_list
		except Exception,e: 
			print "couldn't create/load shelve managed persistent dict".upper()
			print str(e)
			return


	def reload_cache(self, path = DEFAULT_CACHE):
		self.write_cache()
		self.load_cache()

		
	def clear_cache(self, path = DEFAULT_CACHE):
		return


	def write_cache(self, path = DEFAULT_CACHE):
		self.m_cache.close()