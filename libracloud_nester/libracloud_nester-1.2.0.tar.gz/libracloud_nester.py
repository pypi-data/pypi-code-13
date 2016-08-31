#!/usr/local/bin/python3


"""
Module to process lists, and print their contents out to the standard output.
"""


"""
function which accepts a list as a paremeter, and prints its contents to stdout.
The function checks each item in the list, to see if it is a list itself (list within a list). If true, the function calls itself (recursion).
"""


def print_lol(the_list, level=0):
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, level + 1)
        else:
            for num in range(level):
                print("\t", end=' ')
            print(each_item)




