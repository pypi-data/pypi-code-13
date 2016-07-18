
def openr(lis):
    try:
        with open(lis) as li:
            line = li.readline().strip().split(",")
        lin = {}
        lin['Name'] = line.pop(0)
        lin['Time'] = [clean(i) for i in sorted(set(line))][0:3]
        
        return lin
    except IOError as er:
        print("the file has error: "+er)
def clean(lis):
    if '-' in lis:
        p = '-'
    elif ':' in lis:
        p = ':'
    else:
        return lis
    (o,p) = lis.split(p)
    return (o + '.' + p)
def printf(lis):
    print(openr(lis))
printf("jan.txt")
printf("jul.txt")
printf("mik.txt")
printf("sar.txt")
