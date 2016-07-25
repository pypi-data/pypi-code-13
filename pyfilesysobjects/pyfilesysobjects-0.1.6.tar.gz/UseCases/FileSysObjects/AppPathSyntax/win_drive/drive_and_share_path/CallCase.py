"""Check IEEE1003.1-Chap. 4.2.
"""
from __future__ import absolute_import

import unittest
import os,sys
import platform

from pysourceinfo.PySourceInfo import getPythonPathRel
from filesysobjects.FileSysObjects import setUpperTreeSearchPath,normpathX,getTopFromPathString
from unittest.case import SkipTest


#
#######################
#
class UseCase(unittest.TestCase):
    
    def testCase_drive_and_share_path(self):
        _s = sys.path[:]
        start = os.path.abspath(os.path.dirname(__file__)+os.path.normpath('/a/b/c'))
        top = os.path.dirname(start)
        _res = []
        ret = setUpperTreeSearchPath(start,top,_res) #@UnusedVariable

        myplist = [getTopFromPathString('AppPathSyntax',[os.path.dirname(__file__)+os.sep+start])]
        res = []
        for i in range(len(_res)):
            _p = getPythonPathRel(_res[i],myplist)
            if _p:
                res.append(_p) 
        resx =   ['win_drive\\drive_and_share_path\\a\\b\\c', 'win_drive\\drive_and_share_path\\a\\b']
        res = map(normpathX, res)
        resx = map(normpathX, resx)

        [ sys.path.pop() for x in range(len(sys.path)) ] #@UnusedVariable
        sys.path.extend(_s)
        
        self.assertEqual(resx, res)
        pass


if __name__ == '__main__':
    unittest.main()
