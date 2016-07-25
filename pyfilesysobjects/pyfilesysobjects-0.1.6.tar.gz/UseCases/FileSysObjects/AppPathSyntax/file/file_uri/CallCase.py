"""Check IEEE1003.1-Chap. 4.2.
"""
from __future__ import absolute_import

import unittest
import os,sys
import platform

from pysourceinfo.PySourceInfo import getPythonPathRel,getPythonPathFromSysPath
from filesysobjects.FileSysObjects import setUpperTreeSearchPath,FileSysObjectsException,splitAppPrefix,getAppPrefixLocalPath,getTopFromPathString,unescapeFilePath
from unittest.case import SkipTest


#
#######################
#
class UseCase(unittest.TestCase):
    
    def testCase_file_uri(self):
        
        _s = sys.path[:]

        start0 = os.path.abspath(os.path.dirname(__file__)+os.sep+os.path.normpath('/a/b/c'))
    
        # normalize
        _start_elems = splitAppPrefix(start0)
        start= getAppPrefixLocalPath(_start_elems)

        assert start0 == start

        top = 'file://'+os.path.splitdrive(os.path.abspath(os.path.dirname(__file__)))[1]

        _res = []
        ret = setUpperTreeSearchPath(start,top,_res,**{'ias':True}) #@UnusedVariable
        
        forDebugOnly = sys.path #@UnusedVariable
        
        myplist = [getTopFromPathString('AppPathSyntax',[start])]
        res = []
        for i in range(len(_res)):
            res.append(getPythonPathRel(_res[i],myplist)) 

        resx = [
            'file/file_uri/a/b/c', 
            'file/file_uri/a/b', 
            'file/file_uri/a', 
            'file/file_uri'
        ]
        resx = map(os.path.normpath,resx)

        [ sys.path.pop() for x in range(len(sys.path)) ] #@UnusedVariable
        sys.path.extend(_s)
        
        assert resx == res
        pass

    def file_multiple_uri(self):

        if platform.system() != 'Windows':
            unittest.SkipTest("Requires Windows - skipped!")
            return True
       
        _s = sys.path[:]

        _share,start = os.path.splitdrive(os.path.abspath(os.path.dirname(__file__))+os.path.normpath('/a/b/c'))
        _share,top = os.path.splitdrive(os.path.abspath(os.path.dirname(__file__))+os.path.normpath('/a'))
        top = 'file://'+top
        _res = []
        ret = setUpperTreeSearchPath(start,top,_res,**{'ias':True}) #@UnusedVariable
        
        forDebugOnly = sys.path #@UnusedVariable
        
        myplist = [getTopFromPathString('AppPathSyntax',[start])]
        res = []
        for i in range(len(_res)):
            res.append(getPythonPathRel(_res[i],myplist)) 

        resx = [
            'file/file_uri/a/b/c', 
            'file/file_uri/a/b', 
            'file/file_uri/a', 
            'file/file_uri'
        ]
        resx = map(os.path.normpath,resx)

        [ sys.path.pop() for x in range(len(sys.path)) ] #@UnusedVariable
        sys.path.extend(_s)
        

        assert resx == res
        pass

    def file_app(self):
        apstr = 'file://///'+os.path.normpath('hostname/share/a/b/c')
        retRef = ('SHARE','hostname', 'share', os.path.normpath('a/b/c')) 
        ret = splitAppPrefix(apstr)
        self.assertEqual(retRef, ret) 


if __name__ == '__main__':
    unittest.main()
