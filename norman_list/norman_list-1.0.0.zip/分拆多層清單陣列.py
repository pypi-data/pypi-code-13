def alist(清單):
    '''這是分拆多層清單陣列的迴圈程式碼'''
    for a in 清單:
        if isinstance(a,list):
            alist(a)
        else:
            print(a)
