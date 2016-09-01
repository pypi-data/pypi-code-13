'''
Created on 09/03/2016

@author: MMPE
'''
import unittest

from wetb.wind.air_density import air_density, saturated_vapor_pressure2, \
    saturated_vapor_pressure, saturated_vapor_pressure3, saturated_vapor_pressure4, \
    saturated_vapor_pressure_IEC


class Test(unittest.TestCase):


    def test_vapor_pressure(self):
        self.assertAlmostEqual(saturated_vapor_pressure(25), 31.67008, 5)
        self.assertAlmostEqual(saturated_vapor_pressure2(25), 31.67008, 2)
        self.assertAlmostEqual(saturated_vapor_pressure3(25), 31.67008, 1)
        self.assertAlmostEqual(saturated_vapor_pressure4(25), 31.67008, 2)
        self.assertAlmostEqual(saturated_vapor_pressure_IEC(25), 31.67008, delta=0.6)


    def testAirDensity(self):
        self.assertAlmostEqual(air_density(1013, 25, 100), 1.1696, 4)
        self.assertAlmostEqual(air_density(1000, 0, 0), 1.2754, 4)
        self.assertAlmostEqual(air_density(1013.25, 15, 0), 1.225, 4)
        self.assertAlmostEqual(air_density(1013, 20, 49), 1.1987, 4)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testAirDensity']
    unittest.main()
