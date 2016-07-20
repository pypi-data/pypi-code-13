"""This is the "nester.py" module, and it provides one function called
print_lol() which prints lists that may or not include nested lists."""
import sys

def print_lol(the_list, indent=False, level=0, fh=sys.stdout):
    """This function takes a positional argument called "the_listed", which is any
    Python list (of, possibly, nested lists). Each data item in the provided list
    is (recursively) printed to the screen on its own line."""
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, indent, level + 1, fh)
        else:
            if indent:
                for tab_stop in range(level):
                    print("\t", end='', file=fh)
            print(each_item, file=fh)
"""movies = [ "The Holy Grail", 1975, "Terry Jones & Terry Gilliam",
91,["Graham Chapman", ["Michael Palin",
"John Cleese", "Terry Gilliam", "Eric Idle",
"Terry Jones"]]]"""

"""with open('aa.txt', 'w') as data:
    print_lol(movies, True, 0)"""
