def print_lol(L):
    for i in L:
        if isinstance(i,list):
            print_lol(i)
        else:
            print(i)
