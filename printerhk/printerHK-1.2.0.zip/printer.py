from builtins import print


def print_list(the_list,level=-1):
    for element in the_list:
        if isinstance(element,list):
            print_list(element,level + 1)
        else:
            for tab_stop in range(level):
                print('\t',end='')
            print(element)
