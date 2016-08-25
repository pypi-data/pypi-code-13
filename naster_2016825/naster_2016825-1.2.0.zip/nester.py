def print_lol(L,level=0):
    for i in L:
        if isinstance(i,list):
            print_lol(i,level+1)
        else:
            for tab_stop in range(level):
                print("\t",end='')
            print(i)
