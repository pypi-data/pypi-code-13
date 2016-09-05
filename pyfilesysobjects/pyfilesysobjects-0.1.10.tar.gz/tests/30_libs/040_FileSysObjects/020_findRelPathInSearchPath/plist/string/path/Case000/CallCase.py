from __future__ import absolute_import
from __future__ import print_function

__author__ = 'Arno-Can Uestuensoez'
__license__ = "Artistic-License-2.0 + Forced-Fairplay-Constraints"
__copyright__ = "Copyright (C) 2010-2016 Arno-Can Uestuensoez @Ingenieurbuero Arno-Can Uestuensoez"
__version__ = '0.0.1'
__uuid__='af90cc0c-de54-4a32-becd-06f5ce5a3a75'

__docformat__ = "restructuredtext en"

import unittest
import os,sys

import testdata

import filesysobjects.FileSysObjects
import pysourceinfo.PySourceInfo

#
#######################
#


class CallUnits(unittest.TestCase):
    
    def __init__(self,*args,**kargs):
        """Creates search path list
        """
        super(CallUnits,self).__init__(*args,**kargs)    

    @classmethod
    def setUpClass(cls):
        super(CallUnits, cls).setUpClass()
        cls._s = sys.path[:]

        # data
        cls.myBase = testdata.mypath+os.sep+"findnodes"

        #
        # prefix from unchanged sys.path
        cls.mySysPathPrefixRaw = pysourceinfo.PySourceInfo.getPythonPathFromSysPath(__file__) #@UnusedVariable
        
        cls.myTestPath0Rel = os.path.normpath('a/b/c/d/e/f/g/h')
        cls.myTestPath1Rel = cls.myTestPath0Rel +os.sep+ cls.myTestPath0Rel
        cls.myTestPath2Rel = cls.myTestPath1Rel +os.sep+ cls.myTestPath0Rel
        
        
        cls.myTestPath0 = cls.myBase+os.sep+cls.myTestPath0Rel #@UnusedVariable
        cls.myTestPath1 = cls.myBase+os.sep+cls.myTestPath1Rel #@UnusedVariable
        cls.myTestPath2 = cls.myBase+os.sep+cls.myTestPath2Rel #@UnusedVariable

    def reset_sys_path(self):
        [ sys.path.pop() for x in range(len(sys.path)) ] #@UnusedVariable
        sys.path.extend(self._s)
    

    def testCase000(self):

        pxn = self.myTestPath1

        rpath = self.myTestPath1[-1:]
        plist = self.myTestPath1[:-1]
        
        px = filesysobjects.FileSysObjects.findRelPathInSearchPath(rpath,plist,subsplit=True)

        self.reset_sys_path()

        self.assertEqual(px, pxn) 
        pass

    def testCase001(self):

        pxn = self.myTestPath1

        rpath = self.myTestPath1[-1:]
        plist = self.myTestPath1[:-1]
        
        px = filesysobjects.FileSysObjects.findRelPathInSearchPath(rpath,plist,subsplit=True)

        self.reset_sys_path()

        assert px == pxn 
        pass

#
#######################
#

if __name__ == '__main__':
    unittest.main()

