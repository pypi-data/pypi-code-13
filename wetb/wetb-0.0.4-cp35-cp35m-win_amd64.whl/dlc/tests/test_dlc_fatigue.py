import unittest

from wetb.dlc.high_level import Weibull
import numpy as np

class Test_DLC_Fatigue(unittest.TestCase):

    def setUp(self):
        pass

    def test_weibull_1(self):
        Vin = 0.0
        Vout = 100
        Vref = 50
        Vstep = .1
        shape_k = 2
        weibull = Weibull(Vref * 0.2, shape_k, Vin, Vout, Vstep)

        # total probability needs to be 1!
        p_tot = np.array([value for key, value in weibull.items()]).sum()
        self.assertAlmostEqual(p_tot, 1.0, 3)

    def test_weibull_2(self):
        Vin = 1.0
        Vout = 100
        Vref = 50
        Vstep = 2
        shape_k = 2
        weibull = Weibull(Vref * 0.2, shape_k, Vin, Vout, Vstep)
        # total probability needs to be 1!
        p_tot = np.array([value for key, value in weibull.items()]).sum()
        self.assertTrue(np.allclose(p_tot, 1.0))


if __name__ == '__main__':
    unittest.main()
