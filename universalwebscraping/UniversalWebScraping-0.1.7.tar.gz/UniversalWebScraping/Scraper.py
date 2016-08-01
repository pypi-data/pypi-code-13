#-*-coding:utf-8 -*-
import os
import io
import urllib
import urllib2
import ssl
from bs4 import BeautifulSoup
from urllib2 import urlopen, URLError, HTTPError
from datetime import datetime

class Scraper(object):
	"""Who scrap the data from website"""
	def __init__(self):
		super(Scraper, self).__init__()
		self.log_output = 'file'

	def GetSoup(self, url , file_name, overwrite=False):
		file_path = self.GetPage(url, file_name, overwrite)
		content = ''
		with io.open(file_path,'r',encoding='utf-8') as f:
		# with io.open(file_path,'r',encoding='iso-8859-11') as f:
			content = f.read()
		return BeautifulSoup(content, 'html.parser')

	def PostPage(self, url, values, name, overwrite = False):
		if not os.path.exists("tmp/"):
			os.makedirs("tmp/")

		path_str = "tmp/" + name

		if not os.path.exists(os.path.dirname(path_str)):
			os.makedirs(os.path.dirname(path_str))

		if not os.path.exists(path_str) or overwrite:
			# url = 'http://www.someserver.com/cgi-bin/register.cgi'
			# values = {'name' : 'Michael Foord',
			# 'location' : 'Northampton',
			# 'language' : 'Python' }
			data = urllib.urlencode(values)
			request = urllib2.Request(url, data)
			request.encoding = 'windows-874'
			f = urlopen(request)
			cookies = f.info()['Set-Cookie']
			with open(path_str, "wb") as local_file:
				local_file.write(f.read())
			return path_str

		# 	# url = 'http://www.admincourt.go.th/admincourt/site/05SearchSuit.html?pages=2&q=&c=1&limit=&L='
		# 	url = 'http://www.admincourt.go.th/admincourt/site/05SearchSuit.html?IsNext=true&q=&c=1&limit=&L='
		# 	request = urllib2.Request(url)
		# 	request.add_header("Cookie", cookies)
		# 	request.encoding = 'windows-874'
		# 	f = urlopen(request)
		# 	with open('tmp/admincourt/3.html', "wb") as local_file:
		# 		local_file.write(f.read())
		# return path_str
		# u = urllib2.urlopen('http://myserver/inout-tracker', data)
		# h.request('POST', '/inout-tracker/index.php', data, headers)

	def PostPageNeedCookies(self, url, values, name, overwrite = False):
		if not os.path.exists("tmp/"):
			os.makedirs("tmp/")

		path_str = "tmp/" + name

		if not os.path.exists(os.path.dirname(path_str)):
			os.makedirs(os.path.dirname(path_str))

		if not os.path.exists(path_str) or overwrite:
			data = urllib.urlencode(values)
			request = urllib2.Request(url, data)
			request.encoding = 'windows-874'
			f = urlopen(request)
			cookies = f.info()['Set-Cookie']
			with open(path_str, "wb") as local_file:
				local_file.write(f.read())
			return cookies

	def GetPageWithCookie(self, url, name, overwrite = False, encoding = 'windows-874', cookies = None):
		if not os.path.exists("tmp/"):
			os.makedirs("tmp/")

		path_str = "tmp/" + name

		if not os.path.exists(os.path.dirname(path_str)):
			os.makedirs(os.path.dirname(path_str))

		if not os.path.exists(path_str) or overwrite:
			request = urllib2.Request(url)
			request.encoding = encoding
			request.add_header("Cookie", cookies)
			f = urlopen(request)
			with open(path_str, "wb") as local_file:
				local_file.write(f.read())
		return cookies

	def GetPage(self, url, name, overwrite = False, encoding = 'windows-874'):
		if not os.path.exists("tmp/"):
			os.makedirs("tmp/")

		path_str = "tmp/" + name

		if not os.path.exists(os.path.dirname(path_str)):
			os.makedirs(os.path.dirname(path_str))

		if not os.path.exists(path_str) or overwrite:
			request = urllib2.Request(url, headers={'User-Agent' : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"})
			# request = urllib2.Request(url)
			request.encoding = encoding
			context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
			f = urlopen(request, context=context)
			with open(path_str, "wb") as local_file:
				local_file.write(f.read())
		return path_str

	def log(self, content, file_name = 'log', file_mode = 'a', log_type = "info"):
		output = self.log_output
		log_mode = {
			"info": "[INFO]: ",
			"error": "[ERROR]: "
		}

		when =  datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		content = when + " " + log_mode[log_type] + content

		if output is "file":
			f = open(file_name, file_mode)
			f.write(content)
			f.write("\n")
			f.close()
		else :
			print content

