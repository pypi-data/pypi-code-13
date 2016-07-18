def clean(lis):
    if '-' in lis:
        p = '-'
    elif ':' in lis:
        p = ':'
    else:
        return lis
    (o,p) = lis.split(p)
    return (o + '.' + p)
def openr(lis):
    with open(lis) as li:
        line = li.readline().strip().split(",")
    return Athlete(line.pop(0),line)
'''class Athlete:
    def __init__(self,aname,atime = []):
        self.name = aname
        self.time = atime
    def top3(self):
        return sorted(set([clean(n) for n in self.time]))[0:3]
    def addTime(self,lis):
        self.time.append(lis)
    def addTimes(self,lis):
        self.time.extend(lis)'''
class Athlete(list):
    def __init__(self,Aname,Atime):
        list.__init__([])
        self.name = Aname
        self.extend(Atime)
    def top3(self):
        return (sorted(set([clean(i) for i in self])))[0:3]
jan = openr("jan.txt")
jan.extend(['2.00','1.20'])
print(jan.name)
print(jan.top3())
