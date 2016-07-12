def wo(lists,num = 0):
    for l in lists:
        if isinstance(l,list):
            wo(l,num+1)
        else:
            for tab in range(num):
                print('\t',end = '')
            print(l)
