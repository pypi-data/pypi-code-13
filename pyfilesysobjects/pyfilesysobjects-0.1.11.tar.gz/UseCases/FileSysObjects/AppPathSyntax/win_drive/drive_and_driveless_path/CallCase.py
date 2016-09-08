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

    def testCase_drive_and_driveless_path(self):

        _s = sys.path[:]
        
        start0 = os.path.abspath(os.path.dirname(__file__)+os.sep+os.path.normpath('/a/b/c'))
        d,p = os.path.splitdrive(start0)
        start1 = os.sep + p
    
        # normalize
        _start_elems = splitAppPrefix(start0,**{'ias':True})
        start= getAppPrefixLocalPath(_start_elems)

        assert start0 == start
        
        top = 'AppPathSyntax/'
        _res = []
        ret = setUpperTreeSearchPath(start,top,_res,**{'ias':True}) #@UnusedVariable

        myplist = [getTopFromPathString('AppPathSyntax',[start])]
        res = []
        for i in range(len(_res)):
            res.append(getPythonPathRel(_res[i],myplist)) 
        resx = [
            'win_drive/drive_and_driveless_path/a/b/c',
            'win_drive/drive_and_driveless_path/a/b',
            'win_drive/drive_and_driveless_path/a',
            'win_drive/drive_and_driveless_path',
            'win_drive',
            '.',
        ]
        resx = map(os.path.normpath,resx)

        [ sys.path.pop() for x in range(len(sys.path)) ] #@UnusedVariable
        sys.path.extend(_s)
        
        assert resx == res
        pass
    
    def testCase_drive_and_driveless_path2(self):

        _s = sys.path[:]
        
        start0 = os.path.abspath(os.path.dirname(__file__)+os.sep+os.path.normpath('/a/b/c'))
        d,p = os.path.splitdrive(start0)
        start1 = os.sep + p
    
        # normalize
        _start_elems = splitAppPrefix(start0)
        start= getAppPrefixLocalPath(_start_elems)

        assert start0 == start
        
        top = 'AppPathSyntax/'
        _res = []
        ret = setUpperTreeSearchPath(start,top,_res,**{'ias':True}) #@UnusedVariable

        myplist = [getTopFromPathString('AppPathSyntax',[start])]
        res = []
        for i in range(len(_res)):
            res.append(getPythonPathRel(_res[i],myplist)) 
        resx = [
            'win_drive/drive_and_driveless_path/a/b/c',
            'win_drive/drive_and_driveless_path/a/b',
            'win_drive/drive_and_driveless_path/a',
            'win_drive/drive_and_driveless_path',
            'win_drive',
            '.',
        ]        
        resx = map(os.path.normpath,resx)

        [ sys.path.pop() for x in range(len(sys.path)) ] #@UnusedVariable
        sys.path.extend(_s)
        
        assert resx == res
        pass


if __name__ == '__main__':
    unittest.main()
