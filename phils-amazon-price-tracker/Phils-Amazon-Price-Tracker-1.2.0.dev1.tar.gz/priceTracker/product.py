#!/usr/bin/env python3
class product(object):
    """docstring for """
    title=""
    Time=0
    price=0
    merch="amazon"
    def __init__(self, title, price, Time,me):
        self.title = title
        self.price = price
        self.Time = Time
        self.merch=me
    def __getstate__(self):
        return self.title,self.price,self.Time,self.merch
    def __setstate__(self,tit,pr,ti,me):
        self.title = tit
        self.price = pr
        self.Time = ti
        self.merch=me
    pass
    def output(self):
        string = "\n Title: " + self.title + "\nPrice: " + self.price + "\nTime of change: " + self.Time + "\nSeller: " + self.merch
        return string
