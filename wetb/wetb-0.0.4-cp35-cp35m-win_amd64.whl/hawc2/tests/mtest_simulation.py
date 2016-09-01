'''
Created on 18/11/2015

@author: MMPE
'''
import unittest
from wetb.hawc2.log_file import LogFile, \
    INITIALIZATION, SIMULATING, DONE, PENDING
import time
from wetb.hawc2 import log_file
import threading
import os
from wetb.hawc2.htc_file import HTCFile
from wetb.hawc2.simulation import Simulation


class TestSimulation(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.tfp = os.path.join(os.path.dirname(__file__), 'test_files/')  # test file path

#    def test_simulation1(self):
#        sim = Simulation(r'C:\mmpe\HAWC2\Hawc2_model/', "htc/short1.htc", r'C:\mmpe\HAWC2\bin\hawc2-123_beta.exe')
#        sim.simulate()
#        print("finish")

    def test_simulation_no_log(self):
        sim = Simulation(r'C:\mmpe\HAWC2\Hawc2_model/', "htc/short1_no_log.htc", r'C:\mmpe\HAWC2\bin\hawc2-123_beta.exe')
        sim.simulate()
        print("finish")



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_logfile']
    unittest.main()
