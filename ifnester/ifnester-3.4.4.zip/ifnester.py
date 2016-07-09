"""This is "ifnester.py" module and it provides
one function called print_bansal() which prints
lists that may or may not include nested lists."""

def print_bansal(list_name):
    """ This function takes one postional argument called
"list_name", which is any python list (of - possibly - nested lists).
Each data item in the privided list is (recursively) printed
to the screen on it's own line."""
    for each_item in list_name:
        if isinstance(each_item, list):
            print_bansal(each_item)
        else:
            print(each_item)
