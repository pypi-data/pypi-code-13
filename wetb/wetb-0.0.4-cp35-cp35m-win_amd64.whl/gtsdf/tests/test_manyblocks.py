'''
Created on 18/02/2016

@author: MMPE
'''
import unittest
from wetb import gtsdf
import os

tfp = os.path.dirname(__file__) + "/test_files/"
class TestManyBlocks(unittest.TestCase):


    def testManyBlocks(self):
        time, data, info = gtsdf.load(tfp + 'many_blocks2.hdf5')
        self.assertAlmostEqual(time[0], 2.01)
        self.assertAlmostEqual(time[1], 2.02)
        self.assertAlmostEqual(time[-1], 87.81)
        self.assertEqual(data.shape, (8580, 193))
        self.assertAlmostEqual(data[10, 10], 0.56488597)
        self.assertAlmostEqual(data[-10, -10], -1.2286288)




if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
