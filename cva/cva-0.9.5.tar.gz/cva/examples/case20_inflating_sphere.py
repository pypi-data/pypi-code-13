# -*- coding: utf-8 -*-
"""
Case 20: inflating sphere using the Minkowski metric
"""

import numpy as np
import cva

def case20_inflating_sphere():
    cva.solve.select(cva.model.inflating_sphere,cva.metric.minkowski)
    
    # We define a geodesic by fixing its two endpoints in the phase space:
    sa = (0.0,0.5,0.0)   # (u,v,w) an event on the equator at ct=0.0
    sb = (1.0,1.0,0.6)   # (u,v,w) an event at the south pole at ct=1.0
    
    steps = 5
    path = cva.solve.run(sa,sb,steps)
    cva.view.draw(path,title="Case 20: Sphere inflating at 50\% light speed")

if __name__ == '__main__':
    case20_inflating_sphere()
