def clean(LL):#传入列表，统一格式
    LI = []
    for L in LL:
        if '-' in L:
            spliter = '-'
        elif ':' in L:
            spliter = ":"
        else:
            spliter = "."
        (s,d) = L.split(spliter)
        LI.append(s+'.'+d)
    return LI
def op(name):#将字符串转换为列表
    with open(name) as date:
        D = date.readline().strip().split(",")
        return D
def printf(t):
    print(clean(op(t)))
printf("jan.txt")
printf("jul.txt")
printf("mik.txt")
printf("sar.txt")
