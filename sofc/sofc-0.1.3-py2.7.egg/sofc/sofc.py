#!/usr/bin/env python
# coding=utf-8
#
# Author:
# Created Time: 2016年07月25日 星期一 23时55分55秒

import urllib
import click
import requests
from pyquery import PyQuery as pq


STYLE = {
    'fore':
    {   # 前景色
     'black'    : 30,   #  黑色
     'red'      : 31,   #  红色
     'green'    : 32,   #  绿色
     'yellow'   : 33,   #  黄色
     'blue'     : 34,   #  蓝色
     'purple'   : 35,   #  紫红色
     'cyan'     : 36,   #  青蓝色
     'white'    : 37,   #  白色
     },

    'back' :
    {   # 背景
     'black'     : 40,  #  黑色
     'red'       : 41,  #  红色
     'green'     : 42,  #  绿色
     'yellow'    : 43,  #  黄色
     'blue'      : 44,  #  蓝色
     'purple'    : 45,  #  紫红色
     'cyan'      : 46,  #  青蓝色
     'white'     : 47,  #  白色
     },

    'mode' :
    {   # 显示模式
     'mormal'    : 0,   #  终端默认设置
     'bold'      : 1,   #  高亮显示
     'underline' : 4,   #  使用下划线
     'blink'     : 5,   #  闪烁
     'invert'    : 7,   #  反白显示
     'hide'      : 8,   #  不可见
     },

    'default' :
    {
        'end' : 0,
    },
}


def use_style(string, mode='', fore='', back=''):
    mode = '%s' % STYLE['mode'][mode] if mode in STYLE['mode'] else ''
    fore = '%s' % STYLE['fore'][fore] if fore in STYLE['fore'] else ''
    back = '%s' % STYLE['back'][back] if back in STYLE['back'] else ''
    style = ';'.join([s for s in [mode, fore, back] if s])
    style = '\033[%sm' % style if style else ''
    end = '\033[%sm' % STYLE['default']['end'] if style else ''
    return '%s%s%s' % (style, string, end)


def get_url(word, page, num, is_tag=False):
    if is_tag == False:
        return u"http://stackoverflow.com/search?page=" + page + \
            "&tab=relevance&pagesize=" + num + "&q=" + urllib.quote_plus(word)
    return u"http://stackoverflow.com/questions/tagged/" + word + \
        "?page=" + page + "&tab=relevance&pagesize=" + num


@click.command()
@click.argument('word', required=True)
@click.option('-p', "--page", default="1", required=False,
              help='Page: 当前页码')
@click.option('-n', "--num", default="15", required=False,
              help='page Number: 每页显示条数')
@click.option('-s', "--simple", default="true", required=False,
              help='Simple: 是否为简单模式，true则只显示标题和URL, 否则显示全部')
@click.option('-t', "--tag", default="false", required=False,
              help='Tag: 是否为标签模式')
def search(word, page, num, simple, tag):
    print("searching...")

    is_tag = False if tag == 'false' else True
    url = get_url(word, page, num, is_tag)
    response = requests.get(url)
    d = pq(response.text)
    results = d("div.question-summary")
    print("len(results) = " + str(len(results)))

    for res in results:
        # 标题
        title = pq("div.result-link span a", res)
        if (len(title)) < 1:
            title = pq("h3 a", res)[0].text.strip()
            href = pq("h3 a", res)[0].get("href")
        else:
            title = title[0].text.strip()
            href = pq("div.result-link span a", res)[0].get("href")

        print("")
        print(use_style(title, back="green", mode="bold"))
        href = "http://stackoverflow.com" + href
        print(href)

        if simple == "true":
            # 简单模式：只显示标题和url
            continue

        # 投票数
        selector = "span.vote-count-post strong"
        item = pq(selector, res)
        if len(item) == 1:
            vote = item[0].text
        else:
            vote = "0"

        # 回答数
        selector = "div.answered-accepted strong"
        item = pq(selector, res)
        if len(item) == 1:
            answer = item[0].text
        else:
            answer = "0"

        desc = pq("div.excerpt", res).text().strip()
        print(use_style("votes = " + vote + " answers = " + answer,
                        back="blue"))
        print(desc)

    # URL print
    print("")
    print("url: " + response.url)


def main():
    search()

if __name__ == "__main__":
    main()
