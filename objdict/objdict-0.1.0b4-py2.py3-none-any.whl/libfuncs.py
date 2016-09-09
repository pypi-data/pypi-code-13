#!/usr/bin/python

# the libfuncs- designed for direct import

# 2 mar 13.  Libfuncs imported to this lib for evaluation.
#  will update docstrings on funcs that are seen as useful

import urllib
import copy

def generateVectEcho():
    vector=[]
    def vectEcho(*parms):
        for parm in parms:
            if isinstance(parm,list) or isinstance(parm,tuple):
                vector.extend(parm)
            else:
                vector.append(parm)
        return vector
    return vectEcho

class Menus(object):
    """docstring for Menus"""
    def __init__(self, label):
        self.label = label

    def sendFields(self):
        """docstring for sendFields"""
        necho=generateVectEcho()
        necho({"sect0":"%sFields-fld" % self.label})
        necho({"list":"f0-f1-f2-f3-f4-"})
        necho({"fld":"f0"},{"type":"d","name":"ifd","len":25})
        necho({"fld":"f1"},{"type":"i","name":"n","label":"Quantity:","len":3,"def":1})
        necho({"fld":"f2"},{"type":"o9"})
        necho({"fld":"f3"},{"type":"t","name":"var","label":"Additional Comments:","len":32})
        necho({"fld":"f4"},{"type":"b","label":"Make a Favourite","name":"fav"})
        necho({"fld":"non"},{"type":"n"})
        return necho()

    def sendItems(self,label):
        """docstring for sendItems"""
        return []

urldecode=urllib.unquote
def libinit(req):
    global theReq,indebug
    theReq=req
    indebug=False
    if not hasattr(req,'sentHeader'):
        theReq.sentHeader=False
    query=req.saltQuery #subprocess_env["QUERY_STRING"]#.split("?")
    #query=req._req.subprocess_env["QUERY_STRING"]#.split("?")
    #echo("qu is "+repr(query))
    if len(query)> 1 and query.find("du=")!= -1:
        indebug=True
        #echo("set it<br>")


def testindebug():
    global indebug
    return indebug


def testSentHeader():
    global theReq
    return theReq.sentHeader


class SaltPage(object):
    pass

def echo(*strs):
    global theReq
    if not theReq.sentHeader:
        theReq.sendHeader() #send_http_header()
        #theReq.sentHeader=True
    for astr in strs:
        if isinstance(astr,SaltPage):
            astr.sendHeader()
        else:
            theReq.write(astr)

def xpand(dat): # could this be better imlemented using ensuredash as it is used in epair????
    if isinstance(dat,list):
        return '-'.join(dat)+"-"
    return dat

def necho(*xs):
    for x in xs:
        if isinstance(x,list):
            for a in x:necho(a)
        elif isinstance(x,dict):
            for key,dat in x.items():
                echo("%s=%s&" %(key,xpand(dat)))
        else:
            echo(x)
    return
def nechoStr(*xs):
    """docstring for nechoStr"""
    res=""
    for x in xs:
        if isinstance(x,list):
            for a in x:
                res+=nechoStr(a)
        elif isinstance(x,dict):
            for key,dat in x.items():
                res+="%s=%s&" %(key,xpand(dat))
            return res
        else:
            return str(x)
    return str(res)

def nechoNew(*xs):
    res=""
    for x in xs:
        res+=nechoStr(x)
    return echo(res)

necho=nechoNew

def toUrlStr(*xs):
    res=''
    for x in xs:
        if isinstance(x,list):
            for a in x:
                res+=toUrlStr(a)
        elif isinstance(x,dict):
            for key,dat in x.items():
                res+=("%s=%s&" %(key,xpand(dat)))
        else:
            echo(x)
    return res

def fmtAmt(fmt,amt):
    return '%.02f' % float(saltInt(amt)/100.)

class MyDict(dict):
    #def a(self):return 'hi'
    def __init__(self,new,**named):
        dict.__init__(self,**named)
        self.update(new)
        return

class DebMode(object):
    modeLogAndDebug=3
    def __init__(self,mode):
        """ mode =0 ..no ouptut
          mode =1 default , output to html
          mode- 2 output to debug log file
          mode = 3, output to both
          """
        self.mode=mode
        return

def debecho(*strs):
    global theReq, indebug

    logging=False
    debbing=indebug
    if strs and isinstance(strs[0],DebMode):
        logging= strs[0].mode in [2,3]
        debbing= (strs[0].mode in [1,3]) and indebug

    if not (debbing or logging):
        return
    if not theReq.sentHeader and debbing:
        theReq.sendHeader() #send_http_header()
        #theReq.sentHeader=True

    out="<br>"
    import datetime
    log= datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S ") + ' '

    for astr in strs:
        if isinstance(astr,DebMode):
            pass
        elif isinstance(astr,SaltPage):
            astr.sendHeader()
        else:
            out+=repr(astr)+' '
            log+=repr(astr)+' '

    if debbing:
        theReq.write(out+"<br>\n")
    if logging:
        logfile=open('/home/saltsafe/logs/'+ str(theReq.hostname)  + '-log.txt','a')
        logfile.write(log +'\n')
        logfile.close()
    return

def defVal(arr,key,defv=''):
    if isinstance(arr,dict):
        if key in arr and arr[key]!='':#.has_key(key):
            return arr[key]
        return defv
    if isinstance(arr,list):
        if len(arr)>key:
            return arr[key]
    # other wise handle legacy non-dict with has_key - used by req handler
    if hasattr(arr,'has_key'):#and arr.has_key(key):
        if arr.has_key(key) and arr[key]!='':
            return arr[key]
        return defv
    return defv
defval=defVal #allow either case

def defAttr(obj,attr,defv=''):
    if hasattr(obj,attr) and getattr(obj,attr):
        return getattr(obj,attr)
    return defv

def saltInt(p,lst=[]):
    if isinstance(p,dict):
        for subp in lst:
            p[subp]=saltInt(defVal(p,subp,0))
        return p
    elif isinstance(p,list):
        np=[]
        for subp in p:
            np.append(saltInt(subp,0))
        return np
    else:
        try:
            return int(str(p))
        except:
            return 0

def saltLong(p,lst=[]):
    if isinstance(p,dict):
        for subp in lst:
            p[subp]=saltLong(defVal(p,subp,0))
        return p
    elif isinstance(p,list):
        np=[]
        for subp in p:
            np.append(saltLong(subp,0))
        return np
    else:
        try:
            return long(str(p))
        except:
            return 0L
def saltConv(func,p,lst=[]):
    if isinstance(p,dict):
        for subp in lst:
            p[subp]=saltConv(defVal(func,p,subp,0))
        return p
    elif isinstance(p,list):
        np=[]
        for subp in p:
            np.append(func,saltConv(subp,0))
        return np
    else:
        try:
            return func(str(p))
        except:
            return 0

def digits(dstr):
    return "".join([dig for dig in dstr if dig in '0123456789'])

phonePadKeys=("0","1","2abcABC","3defDEF","4ghiGHI","5jklJKL"
              ,"6mnoMNO","7pqrsPQRS","8tuvTUV","9wxyzWXYZ","#","*")

def alphaMatch(alpha,dig):
    global phonePadKeys
    #if($n >=strlen($a)) return "";
    return phonePadKeys[saltInt(dig)].find(alpha) != -1

def phonePadAsNum(alpha):
    """translate series of keys on phone to the numbers
    eg  bad => 223-
    uses 1st value from key, so # and * are unmapped """
    global phonePadKeys
    res=''
    for alph in alpha:
        newa=0
        for i,dig in enumerate(phonePadKeys):
            if dig.find(alph)!=-1:
                newa=dig[0]
                break
        res+=str(newa)
    return res

def dictfilter(dic,filt,assertem=False,default=''):
    """ filter dic to hold values for fields listed in filt. if assertem, makesure filts are present"""
    res={}#copy.copy(dic)  #dels=[]
    for key in filt:
        if key in dic:
            res[key]=dic[key]
        elif assertem:
            res[key]=default
    #for key in dels:
    #    del res[key]
    return res

safesplit=lambda x,y: len(x.split(y,1)) ==2 and x.split(y,1) or [x.split(y)[0],""]

def truncate(x, empty=[''], minsz=0):
    """ trunctate values present in the empty list from the end of a list"""
    while len(x) > minsz and x[-1] in empty:del x[-1]
    return x
def padout(x,sz,ext):
    """ pad x with ext val until it has sz elts- does not truncate!!"""
    for i in range(sz-len(x)):
        x.append(ext)
    return x

parse=lambda x: dict([safesplit(elt,'=') for elt in x.split('&')])

noControls=lambda text:''.join([a for a in text if ord(a)>=ord(' ')])

def parseAll(string):
    res={}
    string= string.replace("\n","") # delete any trailing \n
    equates= string.split('&')
    #print 'subs=',equates
    for equate in equates:
        pair= equate.split('=')
        if len(pair) == 2:
            if len(pair[0])>0:
                res[pair[0]] = pair[1]
                #print "n",pair[0],"v",pair[1]
    return res

def py_parseAll(string):
    """ parse that works with sect strings"""

def arrayUrlDecode(theArray):
    return [urldecode(s) for s in theArray]

def phpparse(string):
    res={}
    equates= noControls(string).split("&");
    #//array_walk($equates,"dumpit");
    i= 0;
    for equate in equates:
        pair= equate.split("=")#,$equate);
        if len(pair) == 2:
            if len(pair[0])>0:
                splits=pair[1].split("-")
                if len(splits)>1:
                    if pair[1][-1:]=="-":splits=splits[:-1]#take of last where trailing-
                    res[pair[0]] = arrayUrlDecode(splits)
                    # debecho('arrayurldec',pair,splits,arrayUrlDecode(splits))
                else:
                    res[pair[0]] = urldecode(pair[1])
    return res

def phpto1st(strng,char):
    res=strng.find(char)#strin($str,$chr);
    if res>=0: return res;
    return len(strng);

def phpparseAll(strng,level="0"):
    tmp=strng.split("sect%s=" % level);
    res={}#debecho('tmp',tmp)
    if len(tmp[0])>1:
        res=phpparse(tmp[0])
    for tmpi in tmp[1:]:#($i=1;$i < sizeof($tmp);$i++)
        secHdr,secBody=safesplit(tmpi,"&");
        secLbl,secKey=safesplit(secHdr,"-")
        #debecho("sect lbl,key,body",secLbl,secKey,secBody)
        if secKey=='':
            res[secLbl]=phpparse(secBody)#tmpi[seclen:])#(substr(tmpi,$seclen));
        else:
            sub=secBody.split(secKey+"=")#,substr(tmpi,$seclen));
            #subres="";
            subres=phpparse(sub[0])#;//sub0 may be empty string!
            for subj in sub[1:]: #($j=1;$j<sizeof($sub);$j++)
                lbl,body=safesplit(subj,"&")
                subres[lbl]=phpparse(body)
            res[secLbl]=subres
    #debecho('res',res)
    return res

"""def phpparseAll(strng,level="0"):
    tmp=strng.split("sect%s=" % level);
    debecho('tmp',tmp)
    if len(tmp[0])>1:
        res=phpparse(tmp[0])
    for tmpi in tmp[1:]:#($i=1;$i < sizeof($tmp);$i++)
        seclen=phpto1st(tmpi,"&");
        sect=tmpi[:seclen].split("-")
        if len(sect)==1:
            res[sect[0]]=phpparse(tmpi[seclen:])#(substr(tmpi,$seclen));
        else:
            sub=tmpi[seclen:].split(sect[1]+"=")#,substr(tmpi,$seclen));
            subres="";
            subres=phpparse(sub[0])#;//sub0 may be empty string!
            for subj in sub[1:]: #($j=1;$j<sizeof($sub);$j++)
                # //if(!isset($sub[$i]){dumpit( "sub $sub<br>"
                sublen=phpto1st(subj,"&")
                #// dumpit($sect,"resloop");echo "sub[j]",substr($sub[$j],0,$sublen),"<br>";
                #//$res[$sect[0]][substr($sub[$j],0,$sublen)]=parse(substr($sub[$j],$sublen));
                subres[subj[:sublen]]=parse(subj[sublen:])
            res[sect[0]]=subres;
    return res
"""
def stripOut(theStr,strips):
    """ takes each char in strips and removes it from theStr...returns filtered theStr"""
    return "".join([c for c in list(theStr) if not c in list(strips)])

def str_replace(findtext,reptext,strng):
    return strng.replace(findtext,reptext)

def safeString(level,strng):
    """ this ensures strings are safe in parse strings level 0 is basic safe(doesn break parse).
  //level 1 arraysafe also so prohibits '-' ...
 // level 2 is safe as URL as well as a parse string so no spaces or other url illegals"""
    if(level>9):
        return urllib.quote(strng).replace('-','%2d')#
    if(level==3):
        return urllib.quote(strng)#
    # str_replace("+"," ",str_replace("-","%2D",urlencode($strng)));
    res = str_replace("\"","",strng);
    res = str_replace("'","",res);
    res = str_replace(" & "," n ",res);
    res = str_replace("&","-",res);

    if(level >=1):
        res = str_replace("-","_",res);
    if(level >= 2):# not used anymore
        res = str_replace(" ","_",res);

    return res
def strWithLen(pstr,plen,pfill=' '):
    f=[pfill for i in range(plen-len(pstr))]
    return pstr+''.join(f)
def decorateNonMT(strng,trail=' ',lead=''):
    if strng:
        return lead+strng+trail
    return ''

def nocolon(fld,xsep="-"):
    """if not ":" in fld:
        if not xsep in fld:
            return fld
    xtr= len(fld)==10 and 2 or 0
    return fld[0,2+xtr]+fld[3+xtr,5+xtr]+fld[6+xtr,8+xtr]"""
    fld=str(fld)
    if ':' in fld:
        return fld.replace(':','')
    return fld.replace(xsep,'')

def eTreeFromXML(strng):
    res=dict(name='',attrs={},text='',children=[],root=True)
    stack=[res]
    def openat(name,attrs):
        ascAttrs=dict([(str(a),str(b)) for a,b in attrs.items()])
        curr=stack[-1]
        newone=dict(name=str(name),attrs=ascAttrs,text='',children=[])
        curr['children'].append(newone)
        stack.append(newone)
        return
    def closeone(name):
        """ should check name matches - but stay simplistic for now"""
        stack.pop()
        return
    def settext(data):
        curr=stack[-1]
        curr['text']=str(data)
        return
    import xml.parsers.expat
    p=xml.parsers.expat.ParserCreate()

    p.StartElementHandler = openat
    p.EndElementHandler = closeone
    p.CharacterDataHandler = settext
    p.Parse(strng)
    #kludge fix for root...should look further!
    try:
        root=res['children'][0]
        if not root['attrs']:
            root['attrs']=root['children'][0]['attrs']
            #root['attrs']['path']='/'
    except:
        raise
        pass
    return res


def getrow(tableOrRow):
    if isinstance(tableOrRow,dict):
        return tableOrRow
    assert 'data' in dir(tableOrRow),'no row and not base with dict'
    return tableOrRow.data

def gettable(tableOrRow):
    if not isinstance(tableOrRow,dict):
        return tableOrRow
    assert 'tbl' in dir(tableOrRow),'looks like tblRow but no tbl set'
    return tableOrRow.tbl


def dispName(dispCol):
    """if passed a dictionay- retrieve the 'name' elt- otherwise value passed is returned
    """
    if isinstance(dispCol,dict):
        return defVal(dispCol,'name','missingName')
    return dispCol


def epairGenerator(necho,row):
    """necho is a reference to a closure function with the appropriate environ to build up output
    row is the row to fetch data from"""
    def epair(key,dat,wasteOfSpace=None):
        """ like necho, but with key and data (data can be a list) and 'wasteOfSpace' which was 'rowmode'
        rowmode was->if row is specified, then dat is a field from row. if an empty row is used, then use last row
        now row is from generator so we test the now 'wasteOfSpace' to see the call qualifies as ok or needs fixing
        once all code is converted we can remove wasteOfSpace
        """
        if dat=="": return

        assert wasteOfSpace!=None,"missing third parameter to epair- convert to necho"
        #we could simply do necho({key:dat}) for this case

        assert wasteOfSpace=="","trying to specify row in call to epair- specifying row to epairGenerator"

        dat=row[dat]
        debecho("MB epair Gen dat",key,dat)

        necho({key:dat})
        return
    return epair

if __name__ == '__main__':
    indebug = True

    class PageEmulator(object):
        def write(self,pstr):print pstr.replace('<br>','\n')

    theReq = PageEmulator()
    testurl = ("tt=os&stb=8061&pn=61411541240&"
              "txnref=3181&jnr=1-01e9b7d74bd9bde1&"
            "appver=1.1.15&delMode=3&pick=0&sp=3.0193632410-&"
            "sect0=ord-isq&isq=0&ico=cCappucino&n=1&sz=0&fl=0"
            "&add=&req=&price=300&du=1")
    a = phpparseAll(testurl)
    print 'a is', a

    necho(a)
