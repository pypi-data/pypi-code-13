def clean(lis):
    if '-' in lis:
        spliter = '-'
    elif ':' in lis:
        spliter = ':'
    else:
        return lis
    (o,p) = lis.split(spliter)
    return (o+'.'+p)
def chang(lis):
    try:
        with open(lis) as li:
            return li.readline().strip().split(",")
    except IOError as err:
        print("FileErroe"+err)
        return(None)
def Sort(lis):
    A = sorted(set([float(clean(l)) for l in chang(lis)]))
    return A
def unique(lis):
    T = []
    for t in lis:
        if t not in T:
            T.append(t)
    return T
print(unique(Sort("jan.txt"))[0:3])
print(Sort("jan.txt")[0:3])
print(Sort("jul.txt")[0:3])
print(Sort("mik.txt")[0:3])
print(Sort("sar.txt")[0:3])
