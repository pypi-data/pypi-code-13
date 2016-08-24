import json
import logging
import lxml.html

from fulmar.base_spider import *

logger = logging.getLogger(__name__)

class Handler(BaseSpider):

    def on_start(self):
        logger.error('Start a new project !')

        self.crawl('http://nsqfy.chinacourt.org/swgk/more.php?LocationID=0602010000', callback=self.index_page, crawl_period=67 * 60)

    def index_page(self, response):

        logger.error(response.headers)
        logger.error(response.cookies)
        logger.error(response.text)

        page_lxml = response.page_lxml
        page_lxml.make_links_absolute(response.orig_url)
        urls = page_lxml.xpath('/html/body/table[4]/tr/td[2]/div/table/tr/td/table[2]/tr/td/table[1]/tr/td[2]/a/@href')
        dates = page_lxml.xpath('/html/body/table[4]/tr/td[2]/div/table/tr/td/table[2]/tr/td/table[1]/tr/td[3]/text()')

        for url, date in zip(urls, dates):
            self.crawl(url, callback=self.detail_page, callback_args=[date,], request_number=1, time_period=10)

    def detail_page(self, response, date):
        logger.error('-------------detail page --------------')
        logger.error(date)