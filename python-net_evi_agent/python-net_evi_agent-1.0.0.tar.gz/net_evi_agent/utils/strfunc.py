#!/usr/bin/python
#-*- coding:UTF-8 -*-
def strPartition(str1,str2):
        string_tup=str1.partition(str2)
        return string_tup

def strSplitToDict(dic,line,split_char):
        tup=strPartition(line,split_char)
        key=tup[0].strip()
        value=tup[2].strip()
        dic[key]=value
        return

