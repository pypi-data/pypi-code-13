"""Sample test function"""
import sys
def print_lol(the_list, indent = False, level = 0, fh=sys.stdout):
    """Prints all the elments in the list including that of inner lists.
    To indent inner list set indent = true
    and set starting level of indent by setting the level.
    """
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item,indent, level + 1, fh)
        else:
            if indent == True:
                for tab_stop in range(level):                
                    print("\t",end='',file=fh)
            print(each_item, file=fh)
