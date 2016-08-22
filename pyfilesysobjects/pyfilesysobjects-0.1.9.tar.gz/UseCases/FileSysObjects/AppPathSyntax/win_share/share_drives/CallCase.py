"""Demonstrates the application of hierarchical search paths on shared drives on Microsoft-Windows(TM). 

Type: SHARE

"""
from __future__ import absolute_import

import unittest
import os,sys
import platform

from pysourceinfo.PySourceInfo import getPythonPathRel
from filesysobjects.FileSysObjects import setUpperTreeSearchPath,getAppPrefixLocalPath,getTopFromPathString


#
#######################
#
class UseCase(unittest.TestCase):
    
    def testCase_SharedDriveC(self):
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

        _rtype = 'SHARE'
        _host = 'localhost'
        sp = s+os.sep.join(sp.split(os.sep)[1:5])+s
        #sp = 2*s+os.sep.join(sp.split(os.sep)[1:5])+s
        _share = 'C$'
        top = getAppPrefixLocalPath((_rtype, _host, _share,sp,))

        _res = []
        ret = setUpperTreeSearchPath(start,top,_res,**{'reverse':True,}) #@UnusedVariable
         
        forDebugOnly = sys.path #@UnusedVariable
       
        _rtype = 'SHARE'
        _host = 'localhost'
        _share = 'C$'
        sp = sp
        mystart = getAppPrefixLocalPath((_rtype, _host, _share,sp,))
         
        mystart  = getTopFromPathString(top,[mystart])
        myplist = [mystart,]
        res = []
        for i in range(len(_res)):
            res.append(getPythonPathRel(_res[i],myplist)) 
             
        resx = [
            '.',
            'UseCases',
            'UseCases/FileSysObjects',
            'UseCases/FileSysObjects/AppPathSyntax',
            'UseCases/FileSysObjects/AppPathSyntax/win_share',
            'UseCases/FileSysObjects/AppPathSyntax/win_share/share_drives',
            'UseCases/FileSysObjects/AppPathSyntax/win_share/share_drives/a',
            'UseCases/FileSysObjects/AppPathSyntax/win_share/share_drives/a/b',
            'UseCases/FileSysObjects/AppPathSyntax/win_share/share_drives/a/b/c',
            'UseCases/FileSysObjects/AppPathSyntax/win_share/share_drives/a/b/c/d',
            'UseCases/FileSysObjects/AppPathSyntax/win_share/share_drives/a/b/c/d/b',
            'UseCases/FileSysObjects/AppPathSyntax/win_share/share_drives/a/b/c/d/b/c',
        ]
        resx = map(os.path.normpath,resx)
 
        [ sys.path.pop() for x in range(len(sys.path)) ] #@UnusedVariable
        sys.path.extend(_s)

        assert resx == res
        pass
 
if __name__ == '__main__':
    unittest.main()

