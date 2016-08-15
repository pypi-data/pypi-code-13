from __future__ import absolute_import
from linecache import getline

__author__ = 'Arno-Can Uestuensoez'
__license__ = "Artistic-License-2.0 + Forced-Fairplay-Constraints"
__copyright__ = "Copyright (C) 2010-2016 Arno-Can Uestuensoez @Ingenieurbuero Arno-Can Uestuensoez"
__version__ = '0.0.1'
__uuid__='af90cc0c-de54-4a32-becd-06f5ce5a3a75'

__docformat__ = "restructuredtext en"

import unittest

import filesysobjects.FileSysObjects

#
#######################
#


class CheckNormpathX(unittest.TestCase):

    def __init__(self,*args,**kargs):
        self.printit = False
        super(CheckNormpathX,self).__init__(*args,**kargs)

    def check_normpathX(self,_in,_norm,ty=None):
        if self.printit:
            print 'Test:'
        l0 = len(_in)
        l1 = len(_norm)

        ret0 = filesysobjects.FileSysObjects.normpathX(_in,**{'tpf':ty})
        lr0 = len(ret0)
        if self.printit:
            print "#---l0 ="+str(l0)
            print "#---lr0="+str(lr0)
            print '  _in = "'+ str(_in) +'"'
            for s in _in: print str(s)+" = "+ str(id(s)) + " ord(" + str(ord(s)) + ")  " + str(s)
            print "#---"
            print '  ret0 = "'+ str(ret0) +'"'
            for s in ret0: print str(s)+" = "+ str(id(s)) + " ord(" + str(ord(s)) + ")  " + str(s)
            print "#---"
        self.assertEqual(_norm, ret0) 

