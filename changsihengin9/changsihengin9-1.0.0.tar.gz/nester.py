#!/usr/bin/env python3
#coding:utf-8
'''
This is my frist funcation,big hug
'''


def print_lol(the_list):
    '''
    Start!
    '''
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item)
        else:
            print(each_item)

