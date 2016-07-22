# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import logging
import re
import dateparser
from crawlermaster.utility import Utility
"""
[
    {
        "lstStrKeyword": "cm:techcrunch-news-tags", 
        "strContent": "cm:techcrunch-news-content", 
        "strCrawlDate": "", 
        "strPublishDate": "cm:techcrunch-news-time", 
        "strSiteName": "TECHCRUNCH", 
        "strTitle": "cm:techcrunch-news-title", 
        "strUrl": "cm:techcrunch-news-url"
    }
]
"""
class ConverterForTechcrunchNewsPage:
    
    #建構子
    def __init__(self):
        self.cmUtility = Utility()
        self.lstDicNewsData = []
    
    def convert(self, strHtmlFilePath=None, dicRawData=None):
        logging.info("convert %s"%strHtmlFilePath)
        try:
            dicNews = {}
            dicNews["lstStrKeyword"] = dicRawData["techcrunch-news-tags"]
            strContent = u""
            for strContentPart in dicRawData["techcrunch-news-content"]:
                strContent = strContent + re.sub("\s", " ", strContentPart).strip()
            dicNews["strContent"] = strContent
            dicNews["strCrawlDate"] = self.cmUtility.getCtimeOfFile(strFilePath=strHtmlFilePath)
            dicNews["strPublishDate"] = dateparser.parse(dicRawData["techcrunch-news-pubtime"][0]).strftime("%Y-%m-%d")
            dicNews["strSiteName"] = "TECHCRUNCH"
            dicNews["strTitle"] = dicRawData["techcrunch-news-title"][0]
            dicNews["strUrl"] = dicRawData["techcrunch-news-url"][0]
            self.lstDicNewsData.append(dicNews)
        except Exception as e:
            logging.warning(str(e))
            logging.warning("parse failed skip: %s"%strHtmlFilePath)
        
    def flushConvertedDataToJsonFile(self, strJsonFilePath=None):
        self.cmUtility.writeObjectToJsonFile(dicData=self.lstDicNewsData, strJsonFilePath=strJsonFilePath)
        self.lstDicNewsData = []