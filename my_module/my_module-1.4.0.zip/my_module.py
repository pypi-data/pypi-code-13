"""simple comment for module"""
import sys


def print_list(list_sequence, tab_count=0):
    for inner in list_sequence:
        if isinstance(inner, list):
            if not isinstance(tab_count, int):
                tab_count = 0
            print_list(inner, tab_count + 1)
        else:
            if isinstance(tab_count, int):
                for num in range(tab_count):
                    sys.stdout.write('\t')
            sys.stdout.write(str(inner) + '\n')
