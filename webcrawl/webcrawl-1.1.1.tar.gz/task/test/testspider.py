#!/usr/bin/env python
# coding=utf-8

from webcrawl.spider import SpiderOrigin
from model.data import Test as Data
from model.data import TestPage as Page_Data

TIMEOUT = 120

class SpiderTestOrigin(SpiderOrigin):

    def __del__(self):
        pass

    def __init__(self, queuetype='Local', timeout=-1, worknum=6, tid=0):
        super(SpiderTestOrigin, self).__init__(queuetype=queuetype, timeout=timeout, worknum=worknum, tid=tid)

if __name__ == "__main__":
    pass

