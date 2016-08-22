#!/usr/bin/python
#coding:utf-8
import sys
import requests
import datetime
import argparse
from bs4 import BeautifulSoup
from sqlalchemy.orm import sessionmaker
from sqlalchemy import desc

from create_db import Record
from create_db import db


class Cc(object):

    def __init__(self):
        self.session = sessionmaker(db)() 

    def top(self, num=10):
        # return top num words that user search
        records = self.session.query(Record)\
                .order_by(desc(Record.number))[:num]
        results = []
        title = "\n\t{:<6}{:<20}{:<6}\n".format("ID", "WORD", "COUNTER")
        results.append(title)
        for rd in records:
            line = "\t{:<6}{:<20}{:<6}".format(rd.id, rd.word, rd.number)
            results.append(line)


        return '\n'.join(results)

    def _del(self, id, word=None):
        pass

    def search(self, word):
        means = self._search_from_db(word)
        if not means:
            means = self._search_from_youdao(word)
        return means


    def _search_from_db(self, word):
        # search for db
         record = self.session.query(Record)\
                 .filter(Record.word==word).first()

         means = None
         if record:
             means = record.means
             # update record number and uptime
             record.number += 1
             record.uptime = datetime.datetime.now()
             self.session.commit()
         return means


    def _search_from_youdao(self, word):
        url = 'http://dict.youdao.com/w/eng/'\
                + word + "/#keyfrom=dict2.index"
        try:
            html = requests.get(url).text
        except Exception as e:
            return u"网络存在问题，请稍后再试。"

        soup = BeautifulSoup(html)
        error_zone = soup.find('div', attrs={'class': "error-typo"})
        results = []

        if error_zone:
            results.append(u"\n单词{word}有误,可能的选择:\n"
                    .format(word=word))
            avaiable_words = error_zone.find_all('a')
            for w in avaiable_words:
                results.append("\t\t\t" + w.string)
            return results

        try:
            word_zone = soup.find('div',
                    attrs={"class": "trans-container"})
            lis = word_zone.find('ul').find_all('li')
            for item in lis:
                results.append(item.string)
            results = '\n'.join(results)
            record = Record(word=word, means=results)
            self.session.add(record)
            self.session.commit()
        except Exception as e:
            return u'\n没有找到单词，请自行搜索。'
        return results

    def last(self, num=10):
        # show num dates of searching 
        records = self.session.query(Record)\
                .order_by(desc(Record.uptime))[:num]

        results = []
        title = "\n\t{:<6}{:<20}{:<20}\n".format("ID", "WORD", "UPDATE TIME")
        results.append(title)
        for rd in records:
            line = "\t{:<6}{:<20}{:<20}".format(rd.id, rd.word, rd.uptime.strftime("%Y-%m-%d %H:%M:%S"))
            results.append(line)

        return '\n'.join(results)


def make_cli():
    cc = Cc()
    parser = argparse.ArgumentParser()
    parser.add_argument("word", help="search word", nargs='?', default="nothing")
    parser.add_argument("-t", "--top", help="show top N words of searching")
    parser.add_argument("-l", "--last", help="show the lastest N words of seaching")
    args = parser.parse_args()

    if args.top:
        print cc.top(args.top)
    elif args.last:
        print cc.last(args.last)
    elif args.word:
        print cc.search(args.word)
    else:
        print u"输入格式有误。"


if __name__ == "__main__":
    make_cli()
    
