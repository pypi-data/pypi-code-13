""""This is a nester.py module and it provides a function print_lol which prints lists that may or may not include nested lists"""
def print_lol(the_list,indent=False,level=0):
        """This Function takes the_list, indent and level as positional arguments which can be any python list and a number.
        Each data item in the list is printed (recursively) to its own line and the nested list are indented based upon the whether indent
        is true and the level of indentation"""
        for each_item in the_list:
                if isinstance(each_item, list):
                        print_lol(each_item,indent,level+1)
                else:
                        if indent:
                                for num in range(level):
                                        print("\t", end='')
                        print(each_item)
