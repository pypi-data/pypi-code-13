def alist(b,indent=False,c=0):
    '''這是一個多層陣列清單執行條列取出迴圈程式'''
    for a in b:
        if isinstance(a,list):
            alist(a,indent,c+1)
        else:
            if indent:
                for d in range(c):
                    print("\t", end="")
            print(a)
