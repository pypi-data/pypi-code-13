'''
Created on 06/11/2015

@author: MMPE
'''
import datetime
import os
import unittest

import numpy as np
from wetb.gtsdf import gtsdf
from wetb.gtsdf.unix_time import from_unix
from wetb.signal_processing.time_shift import find_time_shift


class TestTimeShift(unittest.TestCase):


    def test_find_time_shift(self):

        a = np.random.random(100) * 5
        b = a + 5 + np.random.random(100)

        b[20:30] = np.nan
        b[60:70] = np.nan
        ta = np.arange(100)
        tb = ta.copy().astype(np.float)
        tb[:50] -= 5
        tb[50:] += 5
        for start, end, offset in find_time_shift(a, b, ta, tb, [-5, 0, 5], 20):
            #print (start, end, offset)
            tb[start:end] += offset
        #np.testing.assert_array_equal(ta[~np.isnan(b) & ~np.isnan(tb)], tb[~np.isnan(b) & ~np.isnan(tb)].astype(np.int))

    def test_find_time_shift2(self):

        time_ref, ref, _ = gtsdf.load(os.path.dirname(__file__) + "/test_files/wind_info.hdf5")
        time_sig, sig, _ = gtsdf.load(os.path.dirname(__file__) + "/test_files/L01_status2.hdf5")
        sig = sig[:, 1]
        ref = ref[:, 1]
        #time_ref = time_ref[20000:]

        sig[np.abs(np.diff(sig)) > 90] = np.nan
        ref[np.abs(np.diff(ref)) > 90] = np.nan

        for start, stop, offset in find_time_shift(ref, sig, time_ref, time_sig, [-3600, 0, 3600], 2 * 3600):
            #print (start, stop, len(time_sig), offset)
            if from_unix(time_sig[stop - 1]) < datetime.datetime(2014, 8, 24):
                self.assertTrue (offset == -3600 or np.isnan(offset))
            else:
                self.assertTrue (offset == 0 or np.isnan(offset))

            #print (from_unix(time_sig[start]), from_unix(time_sig[stop - 1]), offset)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()