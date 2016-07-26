#!/usr/bin/python
# coding=utf-8
import copy, time
from pymongo import MongoClient
from datetime import timedelta
from datetime import datetime
from webcrawl.request import get
from webcrawl.request import post
from webcrawl.request import getHtmlNodeContent
from webcrawl.request import getXmlNodeContent
from webcrawl.task import retry
from webcrawl.task import index
from webcrawl.task import initflow
from webcrawl.request import getJsonNodeContent
from webcrawl.task import store
from webcrawl.task import timelimit
from webcrawl.task import next, params
from model.setting import withData, datacfg
from testspider import Data, Page_Data
from testspider import TIMEOUT
from testspider import SpiderTestOrigin

#_print, logger = logprint(modulename(__file__), modulepath(__file__))

class SpiderTest(SpiderTestOrigin):

    """
       test 数据爬虫
    """

    def __init__(self, worknum=6, queuetype='Local', timeout=-1, tid=0):
        super(SpiderTest, self).__init__(worknum=worknum, queuetype=queuetype, timeout=timeout, tid=tid)
        self.clsname = self.__class__.__name__

    @initflow('www')
    @next('step3', 'step2')
    def step4(self, rank, additions={}, timeout=TIMEOUT):
        print '------4'
        for one in range(rank):
            if one < 5:
                yield {'rank1': one}
            else:
                yield {'rank2': one}

    @next('step1')
    @params('rank1')
    def step3(self, rank, additions={}, timeout=TIMEOUT):
        print '------3'
        for one in range(rank):
            yield {'rank': one}

    @next('step1')
    @params('rank2')
    @store(withData(datacfg.W), Page_Data.insert, update=True, method='MANY', target='data')
    def step2(self, rank, additions={}, timeout=TIMEOUT):
        print '------2'
        for one in range(rank):
            if one < 8:
                data = Page_Data(cat=['abc', 'cd'], page_url='https://www.google.com/%s' % str(one), page_id=one, atime=datetime.now(), tid=self.tid)
                yield {'rank': one, 'data':data}
            else:
                yield {'rank': one}

    @store(withData(datacfg.W), Data.insert, update=True, method='MANY')
    @timelimit(3)
    def step1(self, rank, additions={}, timeout=TIMEOUT):
        print '------1'
        url = 'http://www.baidu.com/%s' % str(rank)
        format = 'mp3'
        size = 10
        during = 10
        tag = ['a', 'b', 'c']
        name = '哈哈%s' % rank
        desc = ''
        cover = ''
        snum = rank
        src = 'test'
        host = 'www.test.com'
        singer = '小泽'
        page_url = 'http://www.test.com/%s' % str(rank)
        page_id = hash(page_url)
        parent_page_id = 123
        atime = datetime.now()
        data = Data(url=url, format=format, cat=[],
            size=size, during=during, tag=tag, name=name,
            desc=desc, cover=cover, snum=snum, singer=singer,
            src=src, host=host, page_url=page_url,
            page_id=page_id, parent_page_id=parent_page_id,
            atime=atime, tid=self.tid)
        yield data


if __name__ == '__main__':

    print 'start'
    spider = SpiderTest(worknum=6, queuetype='Local')
    spider.fetch('www', 'fetchList', '201612020303', 5)
    spider.statistic()
    print 'end'
