#!/usr/bin/env python3
# lists_all.py
# A simple list viewer for nested items

def print_lol(the_list, indent=False, tab_levels=0):
    ''' takes two arguments, "the_list" ,a list-nested or otherwise.
    Second argument "indent", initally set to FALSE, controls indentation
    Third argument "tab_levels" inserts tab-stops if a nested list is encountered.

    returns each item recursively & on it's own line.
    '''
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, indent, tab_levels + 1)
        else:
            if indent:
                for tab_stop in range(tab_levels):
                    print('\t', end='')

            print(each_item)

