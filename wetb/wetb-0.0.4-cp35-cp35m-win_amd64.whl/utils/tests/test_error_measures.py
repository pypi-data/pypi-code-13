'''
Created on 20/07/2016

@author: MMPE
'''
import unittest
import os
from wetb.utils.error_measures import rms2mean, rms2fit

tfp = os.path.join(os.path.dirname(__file__), 'test_files/')
import numpy as np
class Test(unittest.TestCase):


    def test_rms2mean(self):
        data = np.load(tfp + "wsp_power.npy")
        print (data.shape)
        wsp = data[:, 1].flatten()
        power = data[:, 0].flatten()

        import matplotlib.pyplot as plt
        plt.plot(wsp, power, '.')
        x = np.linspace(wsp.min(), wsp.max(), 100)
        err, f = rms2mean(wsp, power)
        plt.plot(x, f(x), label='rms2mean, err=%.1f' % err)
        err, f = rms2fit(wsp, power, bins=20, kind=3, fit_func=np.median)
        plt.plot(x, f(x), label='rms2median, err=%.1f' % err)
        print (list(x))
        print (list(f(x)))
        plt.legend()
        plt.show()



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_rms2mean']
    unittest.main()
