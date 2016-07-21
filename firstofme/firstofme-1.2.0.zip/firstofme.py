def printss(the_list, level=0):
    """print each item of the list."""
    for each_item in the_list:
        if isinstance(each_item, list):
            printss(each_item, level+1)

        else:
            for tab_stop in range(level):
                print("\t", end='')
            print(each_item)

