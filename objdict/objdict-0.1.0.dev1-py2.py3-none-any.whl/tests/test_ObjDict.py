#
from __future__ import (absolute_import, division,
                        print_function) #, unicode_literals)
import decimal
from  objdict import objdict

from objdict.objdict import (json,loader, #encode, #"decode", #,jsParse,unParse
                        ObjectEncoderAll,ObjectEncoderStd,
                         ObjDict)
from collections import OrderedDict
import json
from bson.objectid import ObjectId  #used to test including ObjectId
import pytest


# class Fred:
#     def __init__(self,a,b):
#         self.a=a
#         self.b=b

def jsParse(strng,DefaultType=ObjDict):
    return loader(strng  ,object_pairs_hook=ObjDict,
         DefaultType=DefaultType, parse_float=decimal.Decimal)

def unParse(obj,skip={},include={} , **nparms):
    """unParse serialises obj - putting in URL format if url= true
        url case has data limitations compared to json
        and escaping '=' characters otherwise to elimate confusions with urls
        passing 'indent'' (e.g indent = 4) formats the output but can be read
        skip and include at dictionaries or items of types to include or skip
        allObjs=True  will return 'str(obj) for any object that
                    raises a type error tyring to unParse.
                    Beware is unexpect str for obj
    """

    ObjectEncoder = ObjectEncoderAll if nparms.pop(
                            'allObj',False) else ObjectEncoderStd

    #return = json.dumps(obj, cls=ObjectEncoder, **nparms)
    return objdict.dumper(obj, cls=ObjectEncoder, **nparms)


@objdict.from_json()
class DataModel2(ObjDict):
  pass


@objdict.to_json()
class OutExample:
  @objdict.handler
  def handler(self):
    print('called handler')
    return {"a":1}

@objdict.to_json()
@objdict.from_json()
class DataModel(object):
    def __init__(self, id=0, value=7,**kwargs):
        #print('kwargs',kwargs)
        self.id = id
        self.value = value
    def __repr__(self):
        return '<DM id:{id} val:{value}>'.format(**self.__dict__)

@pytest.fixture
def datamodel():
    return DataModel()

@pytest.fixture
def tobj():
    return ObjDict(a=5,b=3)

@objdict.from_json()
class SubClassWithInit(ObjDict):
    def __init__(self,a=None,b=None,**kwargs):
        print('kwargs',kwargs)
        super(SubClassWithInit,self).__init__()
        self.a=a
        self.b=b
        self.c=kwargs

@pytest.fixture
def ordlist():
    return [('a',1),('b',2),('c',3)]

class TestObjDict:
    def test_attrib(self,tobj):
        #tobj=ObjDict(a=5,b=3)
        assert tobj.a==5

    def test_set_type(self,tobj):
        # _set_type defaults to false but can be set to true
        assert tobj._set_type == False
        tobj._set_type = True
        assert tobj._set_type == True

    def test_dictv(self,tobj):
        #check intial dictionay value
        assert tobj['a']==5

    def test_addatrrib(self,tobj):
        #add new attribute and check access by dictionary
        tobj.c=10
        assert tobj['c']==10

    #@pytest.mark.xfail
    def test_add_hidden_atrrib(self,tobj):
        with pytest.raises(KeyError):
            tobj._c=10
            assert tobj['_c']==10

    def test_addtodict(self,tobj):
        tobj['c'] = 10
        assert tobj.c ==10
        assert tobj['c']== 10 #did we break std ?

    def test_initlist(self,ordlist):
        o=ObjDict(ordlist)
        assert list(o.keys())==['a','b','c']

    def test_initsequence(self):
        tobj=SubClassWithInit(a=1,b=2)
        tobj.c=3
        tobj.d=4
        tobj.f=5
        tobj.e=6
        assert list(tobj.keys())==['a','b','c','d','f','e']


    #def test_init_fromObjDict(self,tobj):


@objdict.to_json()
@objdict.from_json()
class SampleClass:
    def __init__(self,a=None,b=None):
        self.a=a
        self.b=b
class SubClass(ObjDict):
    pass

@objdict.from_json()
class SubSimpleClass(ObjDict):
    def __init__(self,*args,**kwargs):
        #manual ordering plus default
        print('argslook',args)
        super(SubSimpleClass,self).__init__(*args,**kwargs)
class RawClass:
    pass
@pytest.fixture
def sample_text():
    return """
    {
    "zeroth":{ "type": "justdict","a":1,"b":2},
    "first":{ "__type__": "SampleClass","a":1,"b":2},
    "second":{ "__type__": "Test2","a":1,"b":2},
    "third": {"__type__": "RawClass"},
    "forth": { "a":1,"b":2,"__type__": "SubSimpleClass"},
    "fifth": {"__type__": "SubClassWithInit", "a":1,"b":2,"c":3}
    }
    """
@pytest.fixture
def parsed_text(sample_text):
    return jsParse(sample_text)

class TestInstanceJson:
    def test_with_types(self,parsed_text):
        t= parsed_text
        assert isinstance(t['zeroth'],ObjDict)
        assert t['zeroth']._set_type==False
        print('type',type(t['second']),type(t['first']),SampleClass)
        #assert False
        assert isinstance(t['first'],SampleClass)
        assert isinstance(t['second'],ObjDict)
        assert t['second']._set_type==True

        # now test class name is preserved
        assert t['second'].__class__.__name__ == "Test2"
        assert t['third'].__class__.__name__ == "RawClass"
        print('5 keys',list(t['fifth'].keys()))
        assert list(t['fifth'].keys()) == ["a","b","c"]
        assert t['fifth'].c =={} #at some time want something to keep


    def test_with_autotypes_order(self,parsed_text):
        t= parsed_text
        print('for',t['forth'].keys())
        assert t['forth'].keys() != ["__type__","b","a",]#["a","b","__type__"]

    @pytest.mark.xfail
    def test_name_collide(self,sample_text):
        """ instanced classes do not match existing classes if the
          existing class is not decorated to expect to be used for json data
         """
        t=jsParse(sample_text)
        print('raw',type(t['third']),RawClass)
        assert isinstance(t['third'],RawClass)


@pytest.fixture
def complexObj():
    foo=DataModel(1,'silly')
    cord= ObjDict([('aa',1),('bb',2),('cc',3),('dd',4)])
    data = {'a':5.6  ,'b':DataModel(5, foo)
            ,'c':cord}
    return data


class TestUnParse:
    def test_odict(self,complexObj):
        print('dat',complexObj['c'])
        dumdat=objdict.dumper(complexObj)
        print('dumper',dumdat)
        d2=loader(dumdat,object_pairs_hook=ObjDict)
        print('load',d2)
        out=jsParse(dumdat)
        assert list(out['c'].keys()) ==['aa','bb','cc','dd']
    #def test_with_types(self,sample_text)

    def test_ObjDict(self,ordlist):
        o=ObjDict(ordlist)
        s=SubClass(ordlist)
        print ('pro',unParse(o),unParse(s))
        assert unParse(o)=='{"a": 1, "b": 2, "c": 3}'
        s_un=unParse(s)
        #unParse(Fred(1,2))
        assert '__type__' in s_un and 'SubClass' in s_un

    def test_UnParseObjID(self):
        tdata={'a':5,'b':ObjectId()}
        assert '_ObjectId' in unParse(tdata)



# the testing code
if __name__ == '__main__':
    #
    #  Note:  this code no longer used (Feb 2016 io).
    # the following code is from old 'pre-py.test' testing, and could provides
    # raw material for new tests. if a new test is needed, there may be starter
    # code here
    #
    combiParse(sample_text())
    indebug = True
    rawdata=unParse({'a':5.6,'b':{'c':1}
                ,'c':[DataModel(5, [foo])]
                ,'d':cord
                     })
    data=combiParse(rawdata)
    print('rawdat',rawdata,data)
    formdata= unParse(data,indent=4)
    print ('data\n',formdata)

    moddata=formdata.replace('DataModel','DataModel2')

    print(combiParse(formdata))
    modparsed= combiParse(moddata) #,no__type__=True)
    print(modparsed)



    theReq = PageEmulator()

    try:
        with open('parse.txt') as parseFile:
            testmsg = parseFile.read()
    except IOError:
        print ("file parse.txt not found, using internal test\n")
        testmsg = ("tt=os&stb=8061&pn=61411541240&"
              "txnref=3181&jnr=1-01e9b7d74bd9bde1&"
            "appver=1.1.15&delMode=3&pick=0&sp=3.0193632410-&"
            "sect0=ord-isq&isq=0&ico=cCappucino&n=1&sz=0&fl=0"
            "&add=&req=&price=300&du=1")
    #print ("input text to parse")
    a = combiParse(testmsg)
    #print ('a is', a, "\n\n  objwalks\n", objWalk(a), \
    # '\n\njson \n', unParse(a, indent=4))

    #import urllib
    ur=unParse(a)
    #print ('json', ur, '\nurl', urlparselib.urlencode({'json':ur}))

    b=combiParse('{"rc": "0", "stn": "Ju\u003Dra at Rozelle1", "fav": "", "stf": "tDUEN", "stb": "8061", "tag": "wap"} ')


    print ('\n uparse b', unParse(b))

    #necho(a)
