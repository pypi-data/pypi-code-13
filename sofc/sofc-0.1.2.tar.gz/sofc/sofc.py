#!/usr/bin/env python
# coding=utf-8
#
# Author:
# Created Time: 2016年07月25日 星期一 23时55分55秒

import click
from pyquery import PyQuery as pq


__version__ = "0.1"

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


@click.command()
@click.option('-w', default=None, required=True, help='Word: 搜索关键词')
@click.option('-p', default="1", required=False, help='Page: 当前页码')
@click.option('-n', default="15", required=False, help='page Number: 每页显示条数')
@click.option('-s', default="true", required=False,
              help='Simple: 是否为简单模式，true则只显示标题和URL, 否则显示全部')
@click.version_option(version=__version__, )
def cli(w, p, n, s):
    surl = u"http://stackoverflow.com/search?page=" \
        + p + "&tab=relevance&pagesize=" + n + "&q=" + w
    d = pq(url=surl)
    results = d("div.search-result")
    print "len = ", len(results)

    for res in results:
        # 标题
        title = pq("div.result-link span a", res)[0].text.strip()
        href = pq("div.result-link span a", res)[0].get("href")
        href = "http://stackoverflow.com" + href

        print
        print use_style(title, back="green", mode="bold")
        print href

        if s == "true":
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
        print vote
        print "votes =", use_style(vote, back="blue"), \
            " answers =", use_style(answer, back="blue")
        print desc


if __name__ == "__main__":
    cli()
