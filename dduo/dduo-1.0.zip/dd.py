name = [123,'duo',456,"you",["the","one",789,[163749,"Luo","Feng"]]]
def wo(thelist):
    for l in thelist:
        if isinstance(l,list):
            wo(l)
        else:
            print(l)
wo(name)
'''for v in name:
    if isinstance(v,list):
        for t in v:
            if isinstance(t,list):
                for i in t:
                    if isinstance(i,list):
                        for p in i:
                             print(p)
                    else:
                        print(i)
            else: 
                print(t)
    else:
        print(v)
   
p = "bdisfdjkshf"
print(len(p))'''
