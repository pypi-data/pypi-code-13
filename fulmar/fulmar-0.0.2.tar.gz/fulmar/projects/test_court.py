import lxml.html
import logging


from fulmar.base_handler import *

# logger = logging.getLogger(__name__)

class Handler(BaseHandler):

    def on_start(self):
        for i in xrange(2000):
            logger.error('Start a new project !')
            self.crawl('http://rmfygg.court.gov.cn/psca/lgnot/bulletin/page/0_1.html', callback=self.index_page, crawl_period=300)

    def index_page(self, response):
        logger.error('in index page')
        logger.error(response.headers)
        logger.error(response.cookies)

        try:
            page = lxml.html.fromstring(response.content.decode('utf-8'))
            urls_path = ('//*[@id="header"]/div/div[6]/div[1]/div[1]/div[4]/d'
                         'iv[1]/div[2]/div/div[2]/div[1]/table/tr/td[1]/a/@href')
            URL_PRE = 'http://rmfygg.court.gov.cn'
            urls = page.xpath(urls_path)

            logger.info(urls)
            for url in urls:
                url_parts = url.split('/')
                url_id = 'block' + url_parts[-1]
                url_path = '/'.join(url_parts[:-1] + [url_id])
                url = URL_PRE + url_path
                self.crawl(url, callback=self.detail_page)

        except Exception as e:
            logger.error(str(e))
    def detail_page(self, response):
        logger.error('-------------detail page --------------')
        logger.info(str({
            "url": response.url,
        }))