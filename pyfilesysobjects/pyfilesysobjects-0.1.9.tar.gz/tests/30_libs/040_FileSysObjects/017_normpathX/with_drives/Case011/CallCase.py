from __future__ import absolute_import
from linecache import getline


__author__ = 'Arno-Can Uestuensoez'
__license__ = "Artistic-License-2.0 + Forced-Fairplay-Constraints"
__copyright__ = "Copyright (C) 2010-2016 Arno-Can Uestuensoez @Ingenieurbuero Arno-Can Uestuensoez"
__version__ = '0.0.1'
__uuid__='af90cc0c-de54-4a32-becd-06f5ce5a3a75'

__docformat__ = "restructuredtext en"

import unittest
import os
import tests.CheckNormpathX

import filesysobjects.FileSysObjects

#
#######################
#

class CallUnits(tests.CheckNormpathX.CheckNormpathX):
    
    def testCase000(self):
        _in        = '\a'
        _norm  = r'\a' 
        self.check_normpathX(_in,_norm,'win')

    def testCase001(self):
        _in        = 'd:/a/b/c'
        _norm  = os.path.normpath('d:\\'+'a\\'+'b\c')  # used as an unaltered reference, thus prep it
        self.check_normpathX(_in,_norm,'win')

    def testCase002(self):
        _in        = 'd:a\b\c'
        _norm  = os.path.normpath('d:a/b/c') 
        self.check_normpathX(_in,_norm)

    def testCase010(self):
        _in        = 'd:'
        _norm  = os.path.normpath('d:' )
        self.check_normpathX(_in,_norm)

    def testCase011(self):
        _in        = 'd:/'
        _norm  = 'd:/'
        self.check_normpathX(_in,_norm,'cnp')
        
    def testCase012(self):
        _in        = 'd:/'
        _norm  = 'd:\\'
        self.check_normpathX(_in,_norm,'win')
        
    def testCase013(self):
        _in        = 'd:/'
        _norm  = 'd:/' 
        self.check_normpathX(_in,_norm, 'cnp')
        pass
    
    def testCase014(self):
        _in        = 'd:\\'
        _norm  = os.path.normpath('d:\\' )
        self.check_normpathX(_in,_norm,'win')
        
    def testCase020(self):
        _in        = 'd:///'
        _norm  = os.path.normpath('d:\\')
        self.check_normpathX(_in,_norm,'win')

    def testCase021(self):
        _in        = 'd:\\\\\\'
        _norm  = os.path.normpath('d:\\')
        self.check_normpathX(_in,_norm,'win')

    def testCase022(self):
        _in        = 'd:///'
        _norm  = os.path.normpath('d:\\')
        self.check_normpathX(_in,_norm,'win')

    def testCase023(self):
        _in        = 'd:\\\\\\'
        _norm  = os.path.normpath('d:\\')
        self.check_normpathX(_in,_norm,'win')

    def testCase030(self):
        _in        = 'd:/a\b/c'
        _norm  = os.path.normpath('d:/a/b/c')
        self.check_normpathX(_in,_norm)

    def testCase031(self):
        _in        = 'd:a\b\c'
        _norm  = os.path.normpath('d:a/b/c')
        self.check_normpathX(_in,_norm)


#
#######################
#

if __name__ == '__main__':
    unittest.main()

