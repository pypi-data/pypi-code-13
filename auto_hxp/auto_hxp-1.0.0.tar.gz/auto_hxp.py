def loop(alist,indent = False,level = 0):
    for each in alist:
        if isinstance(each,list):
           loop(each,indent,level+1)
        else:
            if indent: 
                for tab in range(level):
                    print('\t',end = '')
            print(each)
