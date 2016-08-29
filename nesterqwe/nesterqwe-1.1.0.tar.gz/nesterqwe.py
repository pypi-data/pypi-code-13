#!/usr/bin/env python3

"""
This module provide one function called print_lol()
which prints lists that may or not include nested lists.
"""

def print_lol(the_list):
    """
    recursion function to print list from sub-list
    :param the_list:
    :return:
    """
    for item in the_list:
        if isinstance(item, list):
            print_lol(item)
        else:
            print(item)
