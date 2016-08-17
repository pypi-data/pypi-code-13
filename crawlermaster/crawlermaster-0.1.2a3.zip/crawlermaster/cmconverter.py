# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import logging
from scrapy import Selector
from crawlermaster.utility import Utility
from crawlermaster.converter.converterForTechcrunchNewsPage import ConverterForTechcrunchNewsPage

class CmConverter:

    #建構子
    def __init__(self):
        self.dicConverter = {
            "techcrunch_news": ConverterForTechcrunchNewsPage()
        }

    #轉換 raw-data
    def convert(self, strConverterName=None, strHtmlFilePath=None, dicRawData=None):
        self.dicConverter[strConverterName].convert(strHtmlFilePath=strHtmlFilePath, dicRawData=dicRawData)
    
    #輸出轉換過的 raw-data 至 json 檔
    def flushConvertedDataToJsonFile(self, strConverterName=None, strJsonFilePath=None):
        self.dicConverter[strConverterName].flushConvertedDataToJsonFile(strJsonFilePath=strJsonFilePath)