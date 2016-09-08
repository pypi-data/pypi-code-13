from __future__ import absolute_import
from linecache import getline


__author__ = 'Arno-Can Uestuensoez'
__license__ = "Artistic-License-2.0 + Forced-Fairplay-Constraints"
__copyright__ = "Copyright (C) 2010-2016 Arno-Can Uestuensoez @Ingenieurbuero Arno-Can Uestuensoez"
__version__ = '0.0.1'
__uuid__='af90cc0c-de54-4a32-becd-06f5ce5a3a75'

__docformat__ = "restructuredtext en"

import unittest
import os,sys

import filesysobjects.FileSysObjects
import pysourceinfo.PySourceInfo

#
#######################
#


class CallUnits(unittest.TestCase):
    """Network resources IEEE.1003.1/CIFS/SMB/UNC - respect hostname
    Respect 'hostname', which is actual hostname, and a node name.
    """
    @classmethod
    def setUpClass(self):
        self.top = filesysobjects.FileSysObjects.normpathX('hostname/')
        self.start = filesysobjects.FileSysObjects.normpathX('d://hostname/tests//////a/b/hostname//c////////d/tests/b///c')
        
    def testCase000(self):
        startRef = [('LDSYS', '', 'd:', filesysobjects.FileSysObjects.normpathX('/hostname/tests/a/b/hostname/c/d/tests/b/c'))]
        ret = filesysobjects.FileSysObjects.splitPathVar(self.start,appsplit=True)
        self.assertEqual(startRef, ret) 

    def testCase001(self):
        topRef = [('LFSYS', '', '', 'hostname')]
        ret = filesysobjects.FileSysObjects.splitPathVar(self.top,appsplit=True)
        self.assertEqual(topRef, ret) 


    def testCase002(self):
        top0ref=filesysobjects.FileSysObjects.normpathX('d:/hostname')
        topRef = [('LDSYS', '', 'd:', filesysobjects.FileSysObjects.normpathX('/hostname'))]
        top = filesysobjects.FileSysObjects.getTopFromPathString(self.top, [self.start])
        ret = filesysobjects.FileSysObjects.splitPathVar(top,appsplit=True)

        self.assertEqual(top0ref, top) 
        self.assertEqual(topRef, ret) 
        pass


#
#######################
#

if __name__ == '__main__':
    unittest.main()

