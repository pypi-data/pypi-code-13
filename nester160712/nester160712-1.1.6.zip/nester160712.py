import sys

def nester(the_list, level=0, indent=True, output=sys.stdout):
        for each_item in the_list:
                if isinstance(each_item, list):
                        nester(each_item, level+level, indent, output)
                else:
                        if indent:
                                for num in range(level):
                                        print(' ', end='', file=output)
                        print(each_item, file=output)
