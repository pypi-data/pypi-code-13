#!/usr/bin/env python3
import sys

if __package__ is None and not hasattr(sys, 'frozen'):
    # direct call of __main__.py
    import os.path
    path = os.path.realpath(os.path.abspath(__file__))
    sys.path.insert(0, os.path.dirname(os.path.dirname(path)))

import priceTracker

if __name__ =="__main__":
    priceTracker.main(sys.argv[1:])
#analyseTest("https://www.amazon.de/dp/B0176AR5AO/ref=cm_sw_r_tw_dp_aEWtxb2Z3SSGC")
