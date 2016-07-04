import sys
import json
import requests
import time
import hashlib
from hashlib import sha1
import hmac
import urllib

try:
  from urllib.parse import urljoin
except ImportError:
  from urlparse import urljoin

from otpsecure.base				import Base
from otpsecure.otp				import Otp
from otpsecure.pdf				import Pdf
from otpsecure.status			import Status

ENDPOINT	   = 'http://api.otpsecure.net/'
CLIENT_VERSION = '1.0.0'
PYTHON_VERSION = '%d.%d.%d' % (sys.version_info[0], sys.version_info[1], sys.version_info[2])


class ErrorException(Exception):
  def __init__(self, errors):
	self.errors = errors
	message = ' '.join([str(e) for e in self.errors])
	super(ErrorException, self).__init__(message)


class Client(object):
	def __init__(self, apikey, secret):
		self.apikey = apikey
		self.secret = secret
		self._supported_status_codes = [200, 201, 204, 401, 404, 405, 422]

	def request(self, path, method='GET', params={}):
		url = urljoin(ENDPOINT, path)
		
		timestamp = str(int(round(time.time() * 1000)))
		
		data = json.dumps(params,separators=(',', ':'))

		m = hashlib.md5()
		m.update(data)
		md5 = m.digest().encode('base64').rstrip('\n')

		content_type = 'application/json'
		concatenar = method + '\n' + md5 + '\n' + content_type + '\n' + timestamp
		
		hmac_encode = hmac.new(self.secret, urllib.unquote(concatenar), sha1).digest().encode('base64').rstrip('\n')
		hmacstr = 'Hmac %s:%s' % (self.apikey, hmac_encode)

		headers = {
		  'Accept'			: content_type,
		  'date'			: timestamp,
		  'authorization'	: hmacstr,
		  'User-Agent'		: 'otpsecure/ApiClient/%s Python/%s' % (CLIENT_VERSION, PYTHON_VERSION),
		  'Content-Type'	: content_type
		}
		
		print method + ' ' + url
		print hmacstr
		print data

		if method == 'GET':
			response = requests.get(url, verify=True, headers=headers, params=params)
		else:
			response = requests.post(url, verify=True, headers=headers, data=json.dumps(params,separators=(',', ':')))	
				
		if response.status_code in self._supported_status_codes:
			json_response = response.json()
			print json_response
		else:
			response.raise_for_status()

		if 'errors' in json_response:
			raise(ErrorException([Error().load(e) for e in json_response['errors']]))

		return json_response

	def otp(self, params={}):
		"""Retrieve a client token and send otp sms."""
		return Otp().load(self.request('sms', 'POST', params))
		
	def pdf(self, id, params={}):
		"""Retrieve a client pdf by id."""
		return Pdf().load(self.request('pdf/' + id, 'POST', params))
		
	def status(self, token, params={}):
		"""Retrieve a client pdf by id."""
		params.update({'token': token})
		return Status().load(self.request('status', 'POST', params))
