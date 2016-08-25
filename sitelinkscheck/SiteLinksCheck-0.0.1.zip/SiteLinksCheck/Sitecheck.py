import urllib2
import re

class Sitecheck():
	def __init__(self,url):
		self.urlname=url
		self.urlpattern=re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
	
	def getalllinks(self):
		"""" 
		Gets all the links present in the given
		url
		"""
		url=urllib2.urlopen(self.urlname)
		alllinks=[]
		links=self.urlpattern.findall(url.read())
		for link in links:
			a=link.split("'")
			for i in a:
				j=i.split('"')
				for t in j:
					if t[0:4]=="http":
						alllinks.append(t)
		url.close()
		return alllinks
	
	def getinternallinks(self):
		"""" 
		Gets all the internal links present in the given
		url
		"""
		internallinks=[]
		alllinks=[]
		alllinks=self.getalllinks()
		internalpattern=re.compile(self.urlname)
		for i in alllinks:
			if bool(internalpattern.search(i)):
				internallinks.append(i)
		return internallinks
	
	def getbrokeninternallinks(self):
		"""" 
		Fetches all the broken and dead links from the 
		internal links present in the given url
		"""
		internalbrokenlinks=[]
		internallinks=[]
		internallinks=self.getinternallinks()
		for i in internallinks:
			try:
				if urllib2.urlopen(i).getcode()!=200:
					internalbrokenlinks.append(i)
			except urllib2.HTTPError, e:
				internalbrokenlinks.append(i)
		return internalbrokenlinks
	
	def getallbrokenlinks(self):
		"""" 
		Fetches all the broken and dead links from the 
		all the links present in the given url
		"""
		allbrokenlinks=[]
		alllinks=[]
		alllinks=self.getalllinks()
		for i in alllinks:
			try:
				if urllib2.urlopen(i).getcode()!=200:
					allbrokenlinks.append(i)
			except urllib2.HTTPError, e:
				allbrokenlinks.append(i)
		return allbrokenlinks
				
				
if __name__=="__main__":
	z= Sitecheck("https://pypi.python.org/pypi")
	print z.getalllinks()
	print z.getinternallinks()
	print z.getbrokeninternallinks()
	print z.getallbrokenlinks()
	
