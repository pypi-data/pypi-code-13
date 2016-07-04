
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from urllib.parse import quote_plus, urlparse, parse_qs
import time

class GoogleSearch:
    _url_search = "https://www.google.%(tld)s/search?hl=%(lang)s&q=%(query)s&btnG=Google+Search&tbs=%(tbs)s&safe=%(safe)s&tbm=%(tpe)s"

    _mockupData = None
    @staticmethod
    def setMockupMode(mockupFile):
        try :
            GoogleSearch._doesMockupMode = True
            file = open(mockupFile,'r',encoding='utf-8')
            GoogleSearch._mockupData = file.read()
        except Exception as e :
            GoogleSearch._mockupData = str(e)
        if not GoogleSearch._mockupData:
            GoogleSearch._mockupData = 'Error on reading mockup file'


    def get_page(self,url):
        request = Request(url)
        request.add_header('User-Agent','Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)')
        response = urlopen(request)
        html = response.read()
        response.close()
        return html

    def filter_result(self,link):
        try:

            # Valid results are absolute URLs not pointing to a Google domain
            # like images.google.com or googleusercontent.com
            o = urlparse(link, 'http')
            if o.netloc and 'google' not in o.netloc:
                return link

            # Decode hidden URLs.
            if link.startswith('/url?'):
                link = parse_qs(o.query)['q'][0]

                # Valid results are absolute URLs not pointing to a Google domain
                # like images.google.com or googleusercontent.com
                o = urlparse(link, 'http')
                if o.netloc and 'google' not in o.netloc:
                    return link

        # Otherwise, or on error, return None.
        except Exception:
            pass
        return None

    # Returns a generator that yields URLs.
    def search(self,query, tld='com', lang='en', tbs='0', safe='off',  only_standard=False, tpe=''):
        if GoogleSearch._mockupData:
            time.sleep(1)
            response = GoogleSearch._mockupData
            return response
        # Prepare the search string.
        query = quote_plus(query)
        url = self._url_search % vars()
        html = self.get_page(url)
        # Parse the response and process every anchored URL.
        soup = BeautifulSoup(html, 'html.parser')
        anchors = soup.find(id='search').findAll('a')
        for a in anchors:
            # Leave only the "standard" results if requested.
            # Otherwise grab all possible links.
            if only_standard and (not a.parent or a.parent.name.lower() != "h3"):
                continue
            # Get the URL from the anchor tag.
            try:
                link = a.get('href')
            except KeyError:
                continue
            # Filter invalid links and links pointing to Google itself.
            link = self.filter_result(link)
            if not link:
                continue
            return a.parent.parent.prettify()

