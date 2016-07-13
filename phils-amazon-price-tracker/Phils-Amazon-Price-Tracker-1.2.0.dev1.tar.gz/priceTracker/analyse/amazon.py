import datetime
import html2text
from ..product import product
from ..graph import graph
from robobrowser import RoboBrowser
from ..__init__ import pClass
browser = RoboBrowser(user_agent="Mozilla Firefox")
def readList():
    print(pClass.inputfile)
    try:
        with open(pClass.inputfile, 'r') as fp:
            for i, l in enumerate(fp):
                pass
            pClass.linkFileEntries=i+1
            print(pClass.linkFileEntries)
        with open(pClass.inputfile, 'r') as fp:
            for line in fp:
                if line != "\n":
                    print("read link: " + line)
                    pClass.inputList.append(line.replace("\n",""))
                    analyse(line.replace("\n",""))
    except FileNotFoundError:
        if not pClass.inputList:
            print(pClass.inputfile + ":" + pClass.outputfile)
            print("No file -> I got nothing to do :(")
pass
def analyse(s):
    from ..save_data import (save,load,createDir)
    link=s
    print("start analysing website: " + s)
    browser.open(s.replace(" ", ""))
    r = browser.find(id='priceblock_ourprice')
    t = browser.find(id='productTitle')
    try:
        brand = browser.find(id='brand').get_text().strip()
    except AttributeError as e:
        print("es gibt keinen herrsteller ")
        brand = "None"
    try:
        mer = browser.find(id="merchant-info").get_text().strip()
        mer = mer[0:40]
    except Exception:
        print("counldnt find merchant-info, trying to find an author")
        mer = getAuthor()
    t = browser.find_all("tr", class_="item-model-number")
    model = html2text.html2text(str(t)).split()
    try:
        title= "" + str(brand) + " " + str(model[1])
    except IndexError as e:
        print("benutze Titel, da keine Produktnummer gefunden wurde: ")
        title = getDiffTitle(str(brand))
    try:
        m = r.get_text().split()
    except AttributeError as e:
        print("There a multiple price options")
        m = getDiffPrice()
    price =m[1].replace(",", ".")
    print(price)
    ttime = str(datetime.datetime.now())
    p1=product(title,price,ttime,mer)
    path=""
    p = browser.find(id='wayfinding-breadcrumbs_feature_div').get_text().strip().split()
    for pa in p:
        if len(pa)<2 and pa != "&":
            path+="/"
        else:
            path+= "" + pa
    path=path.replace("ä", "ae").replace("ü", "ue").replace("ö", "oe")
    createDir(path)
    print("Product: " + title + "\nPrice: "+ price + "\n" + mer + "\nin: " + path)
    pClass.productList = save(p1,s)
    try:
        stars = browser.find(id='reviewStarsLinkedCustomerReviews').get_text().strip()
    except AttributeError:
        stars = "No star review available"
    graph(str(title),m[0],mer,stars,path,pClass)
pass
def getAuthor():
    p = browser.find(id='byline').get_text().strip()
    mer = p.strip()
    return mer[4:15]
def match_class(target):
    def do_match(tag):
        classes = tag.get('class', [])
        return all(c in classes for c in target)
    return do_match
def getDiffPrice():
    path = browser.find_all(match_class(["a-color-price"]))
    path = html2text.html2text(str(path).replace("[", "").replace("]", "")).split()
    price = str(path[1])
    if price[-1] == "." or price[-1] == "," :
        price = price[0:-1]
        path[1]=price
    if not path:
        return ["Kein Preis gefunden","-1"]
    else:
        return path
def getDiffTitle(brand):
    try:
        p = browser.find(id='detail_bullets_id').get_text().strip().split()
        i = p.index("Modellnummer:")
        e = p.index("ASIN:")
        ti = "".join(p[i+1:e])
        title = "" + brand + " " + ti
    except ValueError:
        try:
            t = browser.find(id='productTitle')
            tt = t.get_text().split()
            title = ""
            for i in tt:
                title = title + " " + i
        except AttributeError:
            print("Looks like you want to track an ebook")
            t = browser.find(id='ebooksProductTitle')
            tt = t.get_text().split()
            title = ""
            for i in tt:
                title = title + " " + i
    return title
