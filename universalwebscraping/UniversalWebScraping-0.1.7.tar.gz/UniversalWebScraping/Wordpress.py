#-*-coding:utf-8 -*-
import hashlib
from CommonWeb import *

class Wordpress(CommonWeb):
	"""docstring for Wordpress"""
	def __init__(self, url):
		super(Wordpress, self).__init__(url)
		self.cur_dir = os.path.dirname(os.path.realpath(__file__))
		# self.log_output = 'stdout'
		self.log(self.url)
		self.log(self.cur_dir)

	def GetSoupFromPage(self, page_factors):
		page_factors = [ str(factor) for factor in page_factors]
		url = '/'.join(page_factors)
		url = self.url + url;
		self.log(url)
		when =  datetime.now().strftime("%Y-%m-%d")
		return self.Gathering(url, os.path.join(when, 'pages', '_'.join(page_factors) + '.html'), True)

	def GetListUrlsFromPage(self, page_factors, div):
		soup = self.GetSoupFromPage(page_factors)
		urls = [a['href'] for a in (recent_items.find('a') for recent_items in soup.findAll('div',{'class':'recent-item'})) if a]
		return urls

	def GetTotalPage(self, page_factors, find):
		soup = self.GetSoupFromPage(page_factors)
		pages = soup.find('span', {'class':'pages'}).getText()
		return int(pages.replace('Page 1 of ', '').replace(',', ''))

	def GetCategory(self, url, find):
		title = str(url.strip('/').split('/')[-1])
		m = hashlib.md5()
		m.update(title)
		title = m.hexdigest()
		soup = self.Gathering(url, os.path.join('contents', title + '.html'), False)
		category = soup.find(find['element'], find['atribute']).getText()
		return category

	def GetContent(self, url, find, which_paragraph = -1):
		title = str(url.strip('/').split('/')[-1])
		m = hashlib.md5()
		m.update(title)
		title = m.hexdigest()
		soup = self.Gathering(url, os.path.join('contents', title + '.html'), False)
		contents = soup.find(find['element'], find['atribute'])
		content = contents.find_all('p')[-1].getText()
		return content

	def GetRealPage(self, url):
		title = str(url.strip('/').split('/')[-1])
		m = hashlib.md5()
		m.update(title)
		title = m.hexdigest()
		soup = self.Gathering(url, os.path.join('contents', title + '.html'), False)
		return soup
