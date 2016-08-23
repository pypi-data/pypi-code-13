def downloadPDF(input):
	from bs4 import BeautifulSoup, SoupStrainer
	import httplib2
	import pdfkit
	import os
	http=httplib2.Http()

	to_crawl=[]
	crawled=[]
	
	s='http://www.geeksforgeeks.org/tag/'+input
	to_crawl.append(s)
	try:
		status, response = http.request(s)
	except:
		print "No results. Try again"
		return
	crawled.append(s)
	co=1
	soup = BeautifulSoup(response,"lxml", parse_only=SoupStrainer('a', href=True))
	for link in soup.find_all('a'):
	    li=link['href']
	    if input in li and li not in crawled and li.find('forums')<0:
	        co+=1
	        to_crawl.append(li)
	
	count=0

	while len(to_crawl):
	    b=to_crawl.pop()
	    if input in b and b not in crawled and b.find('forums')<0:
	        try:
	        	home=os.path.expanduser('~/Documents')
	        	directory=os.path.join(home,input.upper())
	        	#print directory
	        	if not os.path.exists(directory):
    				os.makedirs(directory)
    			filename=directory+"/"+input+"-"+str(count)+".pdf"
    			print "Saving :"+filename
	        	pdfkit.from_url(b, filename)
	        	count=count+1
	        	print count+"PDF successfully created"
	        except:
	        	pass
	        crawled.append(b)
	        try:
	        	status, response = http.request(b)
	        except:
	        	pass
	        soup=BeautifulSoup(response,"lxml", parse_only=SoupStrainer('a',href=True))
	        for link in soup.find_all('a'):   
	                li=link['href']
	                if b.find('http://www.geeksforgeeks.org/')==0 and li not in crawled:
                 		to_crawl.append(li)                    
if __name__=="__main__":
	print "Enter a tag"
	s=raw_input()
	downloadPDF(s)	