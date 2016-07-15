# -*- coding: utf-8 -*-
"""
Case 17: Minkowski metric on a plane
"""

import numpy as np
import cva

def plane_in_r4(s):
    s,x = cva.model.startmodel(s, xdim = 4, periodicity = (False, False))
    u = s[:, 0]
    v = s[:, 1]

    x[:, 0] = u # x
    x[:, 1] = 0 # y
    x[:, 2] = 0 # z
    x[:, 3] = v # ct
    return cva.model.finishmodel(x,s)    

def case17_spacetime_plane():
    cva.solve.select(plane_in_r4,cva.metric.minkowski)
    
    # We define a geodesic by fixing its two endpoints in phase space:
    sa = (0.0,0.0)
    sb = (0.5,1.0)

    steps = 5
    path = cva.solve.run(sa,sb,steps)
    cva.view.draw(path,title="Case 17: Flat spacetime on a plane")

if __name__ == '__main__':
    case17_spacetime_plane()
  
#step 1:  path_integral = 0.577796 after 0.324 seconds
#step 2:  path_integral = 0.004073 after 1.293 seconds
#step 3:  path_integral = 0.000116 after 3.510 seconds
#step 4:  path_integral = 0.000061 after 8.217 seconds
#step 5:  path_integral = 0.000050 after 17.927 seconds
#step 6:  path_integral = 0.000047 after 37.659 seconds
#step 7:  path_integral = 0.000047 after 77.188 seconds
#step 8:  path_integral = 0.000046 after 156.840 seconds
#step 9:  path_integral = 0.000046 after 316.426 seconds
#