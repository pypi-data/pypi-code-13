#!/usr/bin/env python3
import os
class priceTracker(object):
    """docstring for """
    productList=[]
    inputList=[]
    productList=[]
    inputfile=""
    outputfile=""
    linkFileEntries=0
    os.chdir(os.path.expanduser("~"))
    def __init__(self):
        self.inputfile = os.path.abspath("./amazon-tracker") + "/productlist.lst"
        self.outputfile = os.path.abspath("./amazon-tracker")
        self.productList= []
        self.inputList = []
        self.productList = []
        self.linkFileEntries=0
    pass
