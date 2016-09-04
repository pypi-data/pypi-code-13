'''This is "nesterprint"module, provide a function "print_iol", it can print each item of a list(even if it contain a nester list)'''
def print_iol(the_list, level):
    for each_item in the_list:
        if isinstance(each_item, list):
            print_iol(each_item, level + 1)
        else:
            for tab_stop in range(level):
                print("\t", end="")
            print(each_item)
