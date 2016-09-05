def alist(b,c=0):
    '''這是一個多層陣列清單執行條列取出迴圈程式'''
    for a in b:
        if isinstance(a,list):
            alist(a,c+1)
        else:
            for d in range(c):
                print("\t\", end=")
            print(a)
