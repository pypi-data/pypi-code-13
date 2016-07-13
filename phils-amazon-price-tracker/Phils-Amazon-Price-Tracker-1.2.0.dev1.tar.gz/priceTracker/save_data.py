import copyreg
import pickle
import os
from .product import product
from .__init__ import pClass
import sys
os.chdir(os.path.expanduser("~"))
def createDir(dir):
    p = dir.replace("/", "/ ").split()
    for d in range(len(p)):
        x = str(p[0:d+1]).replace("[","").replace("]","").replace("'","").replace(" ","").replace(",","")
        path = os.path.abspath("amazon-tracker") + "/" + x
        try:
            os.mkdir(path)
            print("created Folder")
        except FileExistsError as e:
            print("")
pass
def titleExcists(t):
    for e in range(len(pClass.productList)):
        if pClass.productList[e].title == t:
            return True
    return False
def pickle_an_object(o):
    return product, (o.title,o.price,o.Time,o.merch)
def save(pr,li):
    load()
    if not li:
        print("link is empty")
    elif li not in pClass.inputList or not pClass.inputList:
        with open(pClass.inputfile,"a") as ipf:
            ipf.write("" + li + "\n")
            print("wrote link to linkFile")
    if not pClass.productList:
        pClass.productList.append(pr)
    elif not titleExcists(pr.title) or not pClass.productList or pClass.productList[indixes(pr.title)].price != pr.price:
            pClass.productList.append(pr)
    with open(pClass.outputfile + '/productTracker.pr', 'wb') as fp:
        pickle.dump(len(pClass.productList),fp,-1)
        copyreg.pickle(product, pickle_an_object)
        for ob in pClass.productList:
            pickle.dump(ob,fp,-1)
    print("saved data")
    return pClass.productList
pass
def indixes(t):
    indixes=[]
    for e in range(len(pClass.productList)):
        if pClass.productList[e].title == t:
            indixes.append(e)
    return indixes[-1]
pass
def lenIndexes(t):
    indixes=[]
    for e in range(len(pClass.productList)):
        if pClass.productList[e].title == t:
            indixes.append(e)
    return len(indixes)
pass
def load():
    copyreg.pickle(product, pickle_an_object)
    pClass.productList=[]
    try:
        with open(pClass.outputfile + "/productTracker.pr", 'rb') as fp:
            for _ in range(pickle.load(fp)):
                pr = pickle.load(fp)
                if not pClass.productList:
                    pClass.productList.append(pr)
                elif not titleExcists(pr.title) or not pClass.productList or pClass.productList[indixes(pr.title)].price != pr.price:
                        pClass.productList.append(pr)
                if len(pClass.productList)>100:
                    cleanData()
        print("previous product data available")
    except Exception as e :
        print("No previous product data available: " + str(e))
pass
def cleanData():
    copyreg.pickle(product, pickle_an_object)
    pClass.productList=[]
    with open(pClass.outputfile + "/productTracker.pr", 'wb+') as fp:
        for _ in range(pickle.load(fp)):
            pr = pickle.load(fp)
            if lenIndexes(pr)<15:
                pClass.productList.append(pr)
        pickle.dump(len(pClass.productList),fp,-1)
        copyreg.pickle(product, pickle_an_object)
        for ob in pClass.productList:
            pickle.dump(ob,fp,-1)
    print("cleaned saved data")
    sys.exit(-1)
pass
