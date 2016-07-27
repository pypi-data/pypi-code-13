import urllib2
from bs4 import BeautifulSoup
import urllib

def dnd(mobile):
	url = 'http://www.nccptrai.gov.in/nccpregistry/saveSearchSub.misc'
	values = {'phoneno' : mobile}
	data = urllib.urlencode(values)
	req = urllib2.Request(url, data)
	response = urllib2.urlopen(req) 
	if(response.getcode() == 200):
		the_page = response.read()
		soup = BeautifulSoup(the_page,'html.parser')
		text = soup.findAll("td", { "class" : "GridHeader" })
		if(text[0].get_text().strip() == "The number is registered in NCPR"):
			return True
		else:
			return False