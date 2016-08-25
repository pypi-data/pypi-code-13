def print_lol(L,indent=False,level=0):
    for i in L:
        if isinstance(i,list):
            print_lol(i,indent,level+1)
        else:
            if indent:
                for tab_stop in range(level):
                    print("\t",end='')
            print(i)
