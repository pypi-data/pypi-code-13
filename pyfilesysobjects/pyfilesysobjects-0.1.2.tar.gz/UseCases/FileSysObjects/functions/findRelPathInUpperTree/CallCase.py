"""Check search of a relative filepathname - side-branch - in upper tree.
"""
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

from filesysobjects.FileSysObjects import setUpperTreeSearchPath
from filesysobjects.FileSysObjects import findRelPathInSearchPath
from filesysobjects.FileSysObjects import findRelPathInUpperTree
from pysourceinfo.PySourceInfo import getPythonPathRel

#
#######################
#

class CallUnits(unittest.TestCase):
    

    
    

    def testCase000(self):
        _s = sys.path[:]
        lst = []
        assert setUpperTreeSearchPath(os.path.abspath(os.path.dirname(__file__)),'UseCases',lst)

        epy = findRelPathInSearchPath('test00',lst)
        epy = getPythonPathRel(epy,[os.path.abspath(os.path.dirname(__file__)+'../../../../..')])
        x = os.path.normpath("UseCases/FileSysObjects/functions/test00")
        assert epy == x

        epy1 = findRelPathInUpperTree('test00',os.path.abspath(os.path.dirname(__file__)),'UseCases',lst) 
        epy1 = getPythonPathRel(epy1,[os.path.abspath(os.path.dirname(__file__)+'../../../../..')])
        assert epy == epy1

        [ sys.path.pop() for x in range(len(sys.path)) ] #@UnusedVariable
        sys.path.extend(_s)
                
        pass

    def testCase001(self):
        _s = sys.path[:]
        lst = []
        assert setUpperTreeSearchPath(os.path.abspath(os.path.dirname(__file__)),'UseCases',lst)

        epy = findRelPathInSearchPath('test00.d'+os.path.sep+'test01',lst)
        epy = getPythonPathRel(epy,[os.path.abspath(os.path.dirname(__file__)+'../../../../..')])
        x = "UseCases"+os.path.sep+"FileSysObjects"+os.path.sep+"functions"+os.path.sep+"test00.d"+os.path.sep+"test01"
        assert epy == x

        epy1 = findRelPathInUpperTree('test00.d'+os.path.sep+'test01',os.path.abspath(os.path.dirname(__file__)),'UseCases',lst) 
        epy1 = getPythonPathRel(epy1,[os.path.abspath(os.path.dirname(__file__)+'../../../../..')])
        assert epy == epy1

        [ sys.path.pop() for x in range(len(sys.path)) ] #@UnusedVariable
        sys.path.extend(_s)
        
        pass

    def testCase002(self):
        _s = sys.path[:]
        lst = []
        assert setUpperTreeSearchPath(os.path.abspath(os.path.dirname(__file__)),'UseCases',lst)

        epy = findRelPathInSearchPath('test00.d'+os.path.sep+'test01',lst,matchidx=0)
        epy = getPythonPathRel(epy,[os.path.abspath(os.path.dirname(__file__)+'../../../../..')])
        x = "UseCases"+os.path.sep+"FileSysObjects"+os.path.sep+"functions"+os.path.sep+"test00.d"+os.path.sep+"test01"
        assert epy == x

        epy1 = findRelPathInUpperTree('test00.d'+os.path.sep+'test01',os.path.abspath(os.path.dirname(__file__)),'UseCases',lst) 
        epy1 = getPythonPathRel(epy1,[os.path.abspath(os.path.dirname(__file__)+'../../../../..')])
        assert epy == epy1

        [ sys.path.pop() for x in range(len(sys.path)) ] #@UnusedVariable
        sys.path.extend(_s)
        
        pass

    def testCase003(self):
        _s = sys.path[:]
        lst = []
        assert setUpperTreeSearchPath(os.path.abspath(os.path.dirname(__file__)+os.path.sep+'test'+os.path.sep+'test00.d'),'UseCases',lst)

        epy = findRelPathInSearchPath('test00.d'+os.path.sep+'test01',lst,matchidx=0)
        epy = getPythonPathRel(epy,[os.path.abspath(os.path.dirname(__file__)+'../../../../..')])
        x = "UseCases"+os.path.sep+"FileSysObjects"+os.path.sep+"functions"+os.path.sep+"findRelPathInUpperTree"+os.path.sep+"test"+os.path.sep+"test00.d"+os.path.sep+"test01"
        assert epy == x

        epy1 = findRelPathInUpperTree('test00.d'+os.path.sep+'test01',os.path.abspath(os.path.dirname(__file__)),'UseCases',lst) 
        epy1 = getPythonPathRel(epy1,[os.path.abspath(os.path.dirname(__file__)+'../../../../..')])
        assert epy == epy1

        [ sys.path.pop() for x in range(len(sys.path)) ] #@UnusedVariable
        sys.path.extend(_s)

        pass

    def testCase004(self):
        _s = sys.path[:]
        lst = []
        assert setUpperTreeSearchPath(os.path.abspath(os.path.dirname(__file__)+os.path.sep+'test'+os.path.sep+'test00.d'),'UseCases',lst)

        epy = findRelPathInSearchPath('test00.d'+os.path.sep+'test01',lst,matchidx=1)
        epy = getPythonPathRel(epy,[os.path.abspath(os.path.dirname(__file__)+'../../../../..')])
        x = "UseCases"+os.path.sep+"FileSysObjects"+os.path.sep+"functions"+os.path.sep+"test00.d"+os.path.sep+"test01"
        assert epy == x

        epy1 = findRelPathInUpperTree('test00.d'+os.path.sep+'test01',os.path.abspath(os.path.dirname(__file__)),'UseCases',lst,matchidx=1) 
        epy1 = getPythonPathRel(epy1,[os.path.abspath(os.path.dirname(__file__)+'../../../../..')])
        assert epy == epy1

        [ sys.path.pop() for x in range(len(sys.path)) ] #@UnusedVariable
        sys.path.extend(_s)
        
        pass
    
#
#######################
#

if __name__ == '__main__':
    unittest.main()

