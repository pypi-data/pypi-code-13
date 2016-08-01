#-*-coding:utf-8 -*-
from Scraper import *

class CommonWeb(Scraper):
	"""docstring for CommonWeb"""
	def __init__(self, url):
		super(CommonWeb, self).__init__()
		self.url = url

	def Gathering(self, url, file_name, overwrite=False):
		soup = self.GetSoup(url, file_name, overwrite)
		return soup

