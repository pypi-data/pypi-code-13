from .product import product
from .__init__ import pClass
def countTitle(t):
    indixes=[]
    for e in range(len(pClass.productList)):
        if pClass.productList[e].title == t:
            indixes.append(e)
    return len(indixes)
pass
def lastChange(e=1):
    if e != 1:
        print("Last " + str(e) + " changes:")
    else:
        print("Last change:")
    for x in range(e):
        pLast = pClass.productList[-x]
        print(pLast.output())
pass
def writeDateFile():
    with open(pClass.outputfile + '/dateLastChanged.txt', 'w') as fp:
        fp.write("Last changed: ")
        pLast = pClass.productList[-1]
        fp.write(pLast.output())
pass
