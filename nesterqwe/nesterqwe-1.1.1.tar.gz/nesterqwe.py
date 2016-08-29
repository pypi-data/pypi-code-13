#!/usr/bin/env python3

"""
This module provide one function called print_lol()
which prints lists that may or not include nested lists.
"""

def print_lol(the_list, level=0):
    """
    recursion function to print list from sub-list
    :param the_list:
    :return:
    """
    for item in the_list:
        if isinstance(item, list):
            print_lol(item, level+1)
        else:
            for tab_stop in range(level):
                print("\t", end='')
            print(item)


