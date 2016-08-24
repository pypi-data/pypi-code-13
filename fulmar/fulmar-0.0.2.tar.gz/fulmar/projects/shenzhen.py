import json
import logging
import lxml.html

from fulmar.base_spider import *

# logger = logging.getLogger(__name__)

class Handler(BaseSpider):

    def on_start(self):
        logger.error('Start a new project !')
        data = {'operate': 4,
                'currpage': 0,
                'p': 70,
                'type': 2,
                'p1': 6,
                'p2': 57,
                }
        self.crawl('http://www.bafy.gov.cn/Ajax/newslist/newsList.ashx', callback=self.index_page, data=data, crawl_period=30)

    def index_page(self, response):
        logger.error(response.headers)
        logger.error(response.cookies)
        logger.error(response.text)
        logger.error(response.page_lxml)
        data = json.loads(response.text)['DataSet']
        page_lxml = lxml.html.fromstring(data)
        logger.error(page_lxml.xpath('//table'))

        '''
        try:
            logger.info()
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
        '''

    def detail_page(self, response):
        logger.error('-------------detail page --------------')
        logger.info(str({
            "url": response.url,
        }))