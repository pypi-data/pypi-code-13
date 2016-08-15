"""Check defaults.
"""
from __future__ import absolute_import

import unittest
import os,sys
import platform

from pysourceinfo.PySourceInfo import getPythonPathRel
from filesysobjects.FileSysObjects import setUpperTreeSearchPath,getAppPrefixLocalPath,getTopFromPathString,\
    escapeFilePath


#
#######################
#
class CallUnits(unittest.TestCase):

#TODO:
#     def testCase000(self):
#         _s = sys.path[:]
# 
#         start = os.path.abspath(os.path.dirname(__file__)+'/a//////b///c/d/b/c///')
#         top = os.path.normpath('//tests')
#         _res = []
#         ret = setUpperTreeSearchPath(start,top,_res,**{'reverse':True,'ias':True}) #@UnusedVariable
#         
#         forDebugOnly = sys.path #@UnusedVariable
#         
#         res = []
#         for i in range(len(_res)):
#             res.append(getPythonPathRel(_res[i]))
#             
#         resx = [
#             'tests',
#             'tests/30_libs', 
#             'tests/30_libs/040_FileSysObjects', 
#             'tests/30_libs/040_FileSysObjects/070_setUpperTreeSearchPath', 
#             'tests/30_libs/040_FileSysObjects/070_setUpperTreeSearchPath/800_ieee1003', 
#             'tests/30_libs/040_FileSysObjects/070_setUpperTreeSearchPath/800_ieee1003/Case030', 
#             'tests/30_libs/040_FileSysObjects/070_setUpperTreeSearchPath/800_ieee1003/Case030/a', 
#             'tests/30_libs/040_FileSysObjects/070_setUpperTreeSearchPath/800_ieee1003/Case030/a/b', 
#             'tests/30_libs/040_FileSysObjects/070_setUpperTreeSearchPath/800_ieee1003/Case030/a/b/c', 
#             'tests/30_libs/040_FileSysObjects/070_setUpperTreeSearchPath/800_ieee1003/Case030/a/b/c/d', 
#             'tests/30_libs/040_FileSysObjects/070_setUpperTreeSearchPath/800_ieee1003/Case030/a/b/c/d/b', 
#             'tests/30_libs/040_FileSysObjects/070_setUpperTreeSearchPath/800_ieee1003/Case030/a/b/c/d/b/c',
#         ]
#         resx = map(os.path.normpath,resx)
# 
#         [ sys.path.pop() for x in range(len(sys.path)) ] #@UnusedVariable
#         sys.path.extend(_s)
#         
# 
#         assert resx == res
#         pass

#     def testCase001(self):
#         _s = sys.path[:]
# 
#         start = os.path.abspath(os.path.dirname(__file__)+'/a//////b///c/d/b/c///')
#         top = '//tests'
#         _res = []
#         ret = setUpperTreeSearchPath(start,top,_res,**{'reverse':True,'ias':True}) #@UnusedVariable
#         
#         forDebugOnly = sys.path #@UnusedVariable
#         
#         res = []
#         for i in range(len(_res)):
#             res.append(getPythonPathRel(_res[i]))
#             
#         resx = [
#             'tests',
#             'tests/30_libs', 
#             'tests/30_libs/040_FileSysObjects', 
#             'tests/30_libs/040_FileSysObjects/070_setUpperTreeSearchPath', 
#             'tests/30_libs/040_FileSysObjects/070_setUpperTreeSearchPath/800_ieee1003', 
#             'tests/30_libs/040_FileSysObjects/070_setUpperTreeSearchPath/800_ieee1003/Case030', 
#             'tests/30_libs/040_FileSysObjects/070_setUpperTreeSearchPath/800_ieee1003/Case030/a', 
#             'tests/30_libs/040_FileSysObjects/070_setUpperTreeSearchPath/800_ieee1003/Case030/a/b', 
#             'tests/30_libs/040_FileSysObjects/070_setUpperTreeSearchPath/800_ieee1003/Case030/a/b/c', 
#             'tests/30_libs/040_FileSysObjects/070_setUpperTreeSearchPath/800_ieee1003/Case030/a/b/c/d', 
#             'tests/30_libs/040_FileSysObjects/070_setUpperTreeSearchPath/800_ieee1003/Case030/a/b/c/d/b', 
#             'tests/30_libs/040_FileSysObjects/070_setUpperTreeSearchPath/800_ieee1003/Case030/a/b/c/d/b/c',
#         ]
#         resx = map(os.path.normpath,resx)
# 
#         [ sys.path.pop() for x in range(len(sys.path)) ] #@UnusedVariable
#         sys.path.extend(_s)
#         
# 
#         assert resx == res
#         pass

    def testCase002(self):
        #for now windows only
        if platform.system() != 'Windows':
            unittest.SkipTest("Requires Windows - skipped!")
            return True
        if not os.path.exists('\\\\localhost\\C$'):
            unittest.SkipTest("Requires share for this test - skipped!")
            return True
        
        _s = sys.path[:]

        _rtype = 'SHARE'
        _host = 'localhost'
        _share,sp = os.path.splitdrive(os.path.abspath(os.path.dirname(__file__))+os.path.normpath('/a/b///c/d/b/c///'))
        _share = 'C$'
        start = getAppPrefixLocalPath((_rtype, _host, _share,sp,))

        s = os.sep
        s4 = 4*s
        top = 'temp'+s4
        _res = []
        ret = setUpperTreeSearchPath(start,top,_res,**{'reverse':True}) #@UnusedVariable
        
        forDebugOnly = sys.path #@UnusedVariable
      
        _rtype = 'SHARE'
        _host = 'localhost'
        _share = 'C$'
        sp = sp
        mystart = getAppPrefixLocalPath((_rtype, _host, _share,sp,))
        
        mystart  = getTopFromPathString(top,[mystart])
#        myplist = [escapeFilePath(mystart),]
        myplist = [mystart,]
        res = []
        for i in range(len(_res)):
            res.append(getPythonPathRel(_res[i],myplist)) 
            
        resx = [
            '.', 
            'pyfilesysobjects',
            'pyfilesysobjects\\components', 
            'pyfilesysobjects\\components\\pyfilesysobjects', 
            'pyfilesysobjects\\components\\pyfilesysobjects\\tests', 
            'pyfilesysobjects\\components\\pyfilesysobjects\\tests\\30_libs', 
            'pyfilesysobjects\\components\\pyfilesysobjects\\tests\\30_libs\\040_FileSysObjects', 
            'pyfilesysobjects\\components\\pyfilesysobjects\\tests\\30_libs\\040_FileSysObjects\\070_setUpperTreeSearchPath', 
            'pyfilesysobjects\\components\\pyfilesysobjects\\tests\\30_libs\\040_FileSysObjects\\070_setUpperTreeSearchPath\\800_ieee1003', 
            'pyfilesysobjects\\components\\pyfilesysobjects\\tests\\30_libs\\040_FileSysObjects\\070_setUpperTreeSearchPath\\800_ieee1003\\Case030', 
            'pyfilesysobjects\\components\\pyfilesysobjects\\tests\\30_libs\\040_FileSysObjects\\070_setUpperTreeSearchPath\\800_ieee1003\\Case030\\a', 
            'pyfilesysobjects\\components\\pyfilesysobjects\\tests\\30_libs\\040_FileSysObjects\\070_setUpperTreeSearchPath\\800_ieee1003\\Case030\\a\\b', 
            'pyfilesysobjects\\components\\pyfilesysobjects\\tests\\30_libs\\040_FileSysObjects\\070_setUpperTreeSearchPath\\800_ieee1003\\Case030\\a\\b\\c', 
            'pyfilesysobjects\\components\\pyfilesysobjects\\tests\\30_libs\\040_FileSysObjects\\070_setUpperTreeSearchPath\\800_ieee1003\\Case030\\a\\b\\c\\d', 
            'pyfilesysobjects\\components\\pyfilesysobjects\\tests\\30_libs\\040_FileSysObjects\\070_setUpperTreeSearchPath\\800_ieee1003\\Case030\\a\\b\\c\\d\\b', 
            'pyfilesysobjects\\components\\pyfilesysobjects\\tests\\30_libs\\040_FileSysObjects\\070_setUpperTreeSearchPath\\800_ieee1003\\Case030\\a\\b\\c\\d\\b\\c'
        ]
        resx = map(os.path.normpath,resx)

        [ sys.path.pop() for x in range(len(sys.path)) ] #@UnusedVariable
        sys.path.extend(_s)

        assert resx == res
        pass

if __name__ == '__main__':
    unittest.main()
