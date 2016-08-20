"""simple comment for module"""
import sys


def print_list(list_sequence, indented=False, initial_tabs=0):
    for inner in list_sequence:
        if isinstance(inner, list):
            if not isinstance(initial_tabs, int):
                initial_tabs = 0
            print_list(inner, indented, initial_tabs + 1)
        else:
            if isinstance(initial_tabs, int):
                if indented:
                    for num in range(initial_tabs):
                        sys.stdout.write('\t')
            sys.stdout.write(str(inner) + '\n')
