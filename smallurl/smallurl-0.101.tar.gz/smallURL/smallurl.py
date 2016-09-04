# !/usr/local/bin python
# -*- encoding: utf-8 -*-

"""
make a small url with python

"""

try:
	from urllib.parse import urlencode
except ImportError:
	from urllib import urlencode
import sys
import requests

def make_small(url):
	request_url = 'http://tinyurl.com/api-create.php?' + \
	    urlencode({'url':url})
	return requests.get(request_url).content.decode('utf-8')

def main():
	for tinyurl in map(make_tiny, sys.argv[1:]):
		print tinyurl

if __name__ == '__main__':
	main()