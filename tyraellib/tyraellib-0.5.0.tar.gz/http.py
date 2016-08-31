#!/usr/bin/env python
# encoding: utf-8
import logging

import requests


class HttpBaseObject(object):
    def url_get_content(self, url, data, headers={},
                        proxies=dict(http='socks5://127.0.0.1:1234',
                                     https='socks5://127.0.0.1:1234')):
        print "url: {}".format(url)
        print "data: {}".format(data)
        print "headers: {}".format(headers)
        print "proxy: {}".format(proxies)
        response = requests.request("GET", url, params=data, headers=headers, proxies=proxies)
        if response.status_code == 200:
            return response.text
        else:
            logging.warning('get {} status code: {}'.format(url, response.status_code))
            logging.warning('get {} response: \n{}\n'.format(url, response.content))
            return {}


    def url_post_content(self, url, data, headers={},
                         proxies=dict(http='socks5://127.0.0.1:1234',
                                      https='socks5://127.0.0.1:1234'),
                         params={}):
        response = requests.request("POST", url, data=data, params=params, headers=headers, proxies=proxies)
        if response.status_code == 200:
            return response.text
        else:
            logging.warning('get {} status code: {}'.format(url, response.status_code))
            logging.warning('get {} response: \n{}\n'.format(url, response.content))
            return {}
