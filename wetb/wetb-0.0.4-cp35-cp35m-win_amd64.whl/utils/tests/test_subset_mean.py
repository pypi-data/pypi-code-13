'''
Created on 18/07/2016

@author: MMPE
'''
import unittest

import numpy as np
from wetb import gtsdf
from wetb.utils.geometry import rpm2rads
from wetb.utils.subset_mean import time_trigger, subset_mean, power_mean
import os
tfp = os.path.join(os.path.dirname(__file__), 'test_files/')
class TestSubsetMean(unittest.TestCase):
    def test_time_trigger(self):
        time = np.arange(0, 99.5, .5)
        np.testing.assert_array_equal(time[time_trigger(time, 20)], [0, 20, 40, 60, 80])
        np.testing.assert_array_equal(time[time_trigger(time + .5, 20)], [0, 20, 40, 60, 80])
        np.testing.assert_array_equal(time[time_trigger(time + 100000000.5, 20)], [0, 20, 40, 60, 80])
        np.testing.assert_array_equal(time[time_trigger(time, 20, 20, 60)], [20, 40, 60])
        np.testing.assert_array_equal(time_trigger(np.arange(101), 20), [0, 20, 40, 60, 80, 100])
        time, data, info = gtsdf.load(tfp + "subset_mean_test.hdf5")
        np.testing.assert_array_equal(time_trigger(time, 200), [0, 5000, 10000, 15000])

    def test_subset_mean(self):

        time, data, info = gtsdf.load(tfp + "subset_mean_test.hdf5")
        triggers = time_trigger(time, 100)
        t, p = subset_mean([time, data[:, 0]], triggers).T
        self.assertEqual(t[1], time[2500:5000].mean())
        self.assertEqual(p[1], data[2500:5000, 0].mean())

        triggers[1] = 2501
        t, p = subset_mean([time, data[:, 0]], triggers).T
        self.assertEqual(t[1], time[2501:5000].mean())
        self.assertEqual(p[1], data[2501:5000, 0].mean())

    def test_power_mean(self):
        ds = gtsdf.Dataset(tfp + "subset_mean_test.hdf5")
        triggers = time_trigger(ds.time, 100)
#        import matplotlib.pyplot as plt
#        plt.plot(ds.time, ds('Rot_cor') * 80)
#        plt.plot(ds.time, ds('Power'))
#        plt.plot(ds.time[triggers[:-1]], np.zeros_like(triggers[:-1]) + 800, '.')
#        plt.plot(*subset_mean([ds.time, ds('Power')], triggers).T)
#        pm = lambda power, triggers : power_mean(ds('Power') * 1000, 2.5E7, rpm2rads(ds('Rot_cor')), ds.time, triggers) / 1000
#        t, p = subset_mean([ds.time, ds('Power')], triggers, {1: pm}).T
#        plt.plot(t, p, '--')
#        plt.show()
if __name__ == "__main__":
    unittest.main()