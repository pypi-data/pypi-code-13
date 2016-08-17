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
from crawlermaster.cmselector import CmSelector
from crawlermaster.cmspider import CmSpider
from crawlermaster.cmconverter import CmConverter

class CmParser:

    #建構子
    def __init__(self, strCssJsonFilePath=None):
        self.cmUtility = Utility()
        self.cmSelector = CmSelector(strCssJsonFilePath=strCssJsonFilePath)
        self.cmSpider = CmSpider()
        self.cmConverter = CmConverter()
        
    #檢查 selector 正確性
    def selectorTestParse(self):
        lstDicCssSelector = self.cmSelector.getCssSelectorList()
        lstDicTestResultRawData = []
        for dicCssSelector in lstDicCssSelector:
            dicRawData = {}
            strPageSource = self.cmSpider.spiderTempUrlPage(strUrl=dicCssSelector["sampleUrl"], lstDicPreAction=dicCssSelector["preAction"])
            root = Selector(text=strPageSource)
            lstStrAns = root.css(dicCssSelector["cssRule"]).extract()
            dicRawData["name"] = dicCssSelector["name"]
            dicRawData["cssRule"] = dicCssSelector["cssRule"]
            dicRawData["ans"] = lstStrAns
            dicRawData["sampleAns"] = dicCssSelector["sampleAns"]
            if lstStrAns == dicCssSelector["sampleAns"]:
                dicRawData["isExactPass"] = True
                dicRawData["isExistPass"] = True
            elif dicCssSelector["ansType"] == "exist" and len(lstStrAns) > 0:
                dicRawData["isExactPass"] = False
                dicRawData["isExistPass"] = True
            else:
                dicRawData["isExactPass"] = False
                dicRawData["isExistPass"] = False
            logging.info("selector test result: %s"%dicRawData["name"])
            logging.info("exact pass: %r"%dicRawData["isExactPass"])
            logging.info("exist pass: %r"%dicRawData["isExistPass"])
            lstDicTestResultRawData.append(dicRawData)
        return lstDicTestResultRawData
    
    #本地 html 檔案解析
    def localHtmlFileParse(self, strBasedir=None, strSuffixes=None):
        dicLocalHtmlFilePattern = self.cmSelector.getLocalHtmlFilePatternDic()
        if not strBasedir:
            strBasedir = dicLocalHtmlFilePattern.get("strBasedir", None)
        if not strSuffixes:
            strSuffixes = dicLocalHtmlFilePattern.get("strSuffixes", None)
        lstStrHtmlFilePath = self.cmUtility.getFilePathListWithSuffixes(strBasedir=strBasedir, strSuffixes=strSuffixes)
        lstDicPageRawData = []
        for strHtmlFilePath in lstStrHtmlFilePath:
            #讀取 html 檔案
            with open(strHtmlFilePath, "r") as htmlFile:
                strPageSource = htmlFile.read()
                root = Selector(text=strPageSource)
            #讀取 css 規則
            lstDicCssSelector = self.cmSelector.getCssSelectorList()
            dicRawData = {}
            for dicCssSelector in lstDicCssSelector:
                #解析 html
                lstStrAns = root.css(dicCssSelector["cssRule"]).extract()
                dicRawData[dicCssSelector["name"]] = lstStrAns
            #使用 converter 處理 raw data
            strConverterName = self.cmSelector.getConverterName()
            self.cmConverter.convert(strConverterName=strConverterName, strHtmlFilePath=strHtmlFilePath, dicRawData=dicRawData)
            lstDicPageRawData.append(dicRawData)
        #logging.info("parsed raw-data:\n%s"%self.cmUtility.getJsonifyString(dicData=lstDicPageRawData))
        strJsonFilePath = "raw_data.json"
        self.cmUtility.writeObjectToJsonFile(dicData=lstDicPageRawData, strJsonFilePath=strJsonFilePath)
    
    #輸出 已完成轉換的 raw-data
    def flushConvertedDataToJsonFile(self, strJsonFilePath=None):
        strConverterName = self.cmSelector.getConverterName()
        self.cmConverter.flushConvertedDataToJsonFile(strConverterName=strConverterName, strJsonFilePath=strJsonFilePath)