# -*- coding: utf-8 -*-
import re


escape = {
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#x27;",
    "`": "&#x60;"
}


def urlizesmart(value):
    
    ###去掉<a></a>标签，保留链接
    text = re.sub(ur'''<a.*?href=['"](?P<url>https?://(\w*:\w*@)?[-\w.]+(:\d+)?(/([\w/_.]*(\?\S+)?)?)?)[\w_>].*<\/a>''',
                  '\g<url>',
                  value
              )

    for k,v in escape.iteritems():
        if k in text:
            text = text.replace(k,v)

    ###给链接添加上<a></a>标签
    text = re.sub(ur'https?://(\w*:\w*@)?[-\w.]+(:\d+)?(/([\w/_.]*(\?\S+)?)?)?',
                  lambda m:'''<a href="%s" target="_blank">%s</a>'''%(m.group(),m.group()),
                  text
            )
    return text
