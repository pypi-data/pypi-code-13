# -*- coding: utf-8 -*-
from pyquery import PyQuery as pq
import simplejson as JSON
import re
import time

from newspider.interfaces import *
from newspider.spider import Newspider
from newspider.comm.utils import Utils
# from base.commit import PostSession
# from config import *

'''
微博抓取器
'''

class WeiboFetcher(IntFetcher):

    def __init__(self):
        self.next_page = []

    def fetch_detail_urls(self,htmlContent):
        #print "aaaa"
        htmlContent = Utils.conv2utf8(htmlContent,'GBK')
        #print "bbb"
        #print html
        tag = u"全部"
        l = []

        html = pq(htmlContent)
        array = html(".list14 ul li a")
        i = -1
        for item in array:
            element = pq(item)
            i = i + 1
            if i == 0:
                tag = element.text()
                continue
            if i % 2 == 0:
                continue
            url = element.attr('href')
            # text = element.text()
            l.append((url,{"category":tag}))
        return l

    def start_page(self):
        return [  "http://roll.sohu.com/sports_bak/",#>体育</a></li>
            # "http://roll.sohu.com/yule_bak/",#>娱乐</a></li>
            # "http://roll.sohu.com/it_bak/" ,#IT数码</a></li>
            # "http://roll.sohu.com/auto_bak/",# >汽车</a></li>
            # "http://roll.sohu.com/focus_bak/",#>房产</a></li>
            # "http://roll.sohu.com/women_bak/",#>女性</a></li>
            # "http://roll.sohu.com/fashion_bak/",#>时尚</a></li>
            # #"http://roll.sohu.com/baobao/",# >母婴</a></li>-->
            # "http://roll.sohu.com/health_bak/",# >健康</a></li>
            # "http://roll.sohu.com/cul_bak/",# >文化</a></li>
            # "http://roll.sohu.com/learning_bak/",# >教育</a></li>
            # "http://roll.sohu.com/money_bak/",# >财经</a></li>
            # "http://roll.sohu.com/stock_bak/",# >证券</a></li>
            # "http://roll.sohu.com/games_bak/",# >游戏</a></li>
            # "http://roll.sohu.com/media_bak/",# >媒体</a></li>
            # #"http://roll.sohu.com/city_bak/",# >城市</a></li>
            # #"http://roll.sohu.com/luxury_bak/",# >奢侈品</a></li>
            # #"http://roll.sohu.com/star_bak/",# >评论</a></li>
            # "http://roll.sohu.com/travel/",# >旅游</a></li>
            # #"http://roll.sohu.com/pic/",# >大视野</a></li>
            # #"http://roll.sohu.com/subject_bak/",# >专题</a></li>
          ]

    def next_pages(self):
        return self.next_page

    def getJson(self, temp):
        json_str = temp.replace("FM.view(", "").replace(")</script>", "")
        # print json_str
        json = JSON.loads(json_str)
        return json


class WeiboParser(IntParser):

    def parse(self,tag,htmlContent,extras):

        #print "Receive content from url %s for tag %s|%s" % (extras.get('_url'),extras.get('category'),tag)
        htmlContent = Utils.conv2utf8(htmlContent, 'gbk')
        #print htmlContent
        # html = pq(htmlContent)
        #
        # title = html("#headers div div h1").text()
        # media_url = ''
        # # 判断是否为空,如果是,则认为是个人自媒体的文章,采取另一种解释方式
        # if title is None or title == '':
        #     title = html(".news-title h1").text()
        #     media_name = html(".news-title .writer a").text()
        #     media_url = html(".news-title .writer a").attr("href")
        #     public_time = html(".news-title  .time").text()
        # else:
        #     media_name = html("#media_name").text()
        #     media_url_temp = html("#contentText SCRIPT").text()
        #     if media_url_temp is None or media_url_temp == '':
        #         media_url_temp = html("#contentText script").text()
        #     public_time = html(".timeTag .time").text()
        #     if public_time != '':
        #         timeArray = time.strptime(public_time, u"%Y年%m月%d日%H:%M")
        #         public_time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        #     if media_url_temp is not None and media_url_temp != '':
        #         media_url = self.filterUrl(media_url_temp)
        #
        # contentText = self.filterContentText(html("#contentText").html())
        #
        # data =  {"media_name": media_name, "title": title, "media_url": media_url, "contentText": contentText,
        #         'public_time': public_time}
        #
        # #postSession = PostSession()
        # print "post the title :  %s and url:%s" % title, media_url
        # #postSession.post(POST_URL, data)


    def filterUrl(self, url):
        url.replace(" ", "")
        p = re.compile(r"http[s]?://(?:[a-zA-Z]|[0-9]|[-.]|_|/|(?:%[0-9a-fA-F][0-9a-fA-F]))+")
        match = p.findall(url)
        if match:
            print "match %s" % match[0]
            return match[0]
        else:
            return url

    def filterContentText(self, contentText):
        return contentText.strip().replace("\n", '').replace('\t', '')




if __name__ == '__main__':
    sp = Newspider()
    sp.config("USER_AGENT","Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html")
    sp.config('GUARD_INTERVAL', 0)
    sp.config('DEBUG', True)


    sp.add_parser(WeiboParser())
    sp.add_fetcher(WeiboFetcher())

    sp.run()

