# -*- coding: utf-8 -*-
"""
Case 19 collapsing sphere using the Minkowski metric
"""

import numpy as np
import cva

def case19_collapsing_sphere():
    cva.solve.select(cva.model.collapsing_sphere,cva.metric.minkowski)
    
    # We define a geodesic by fixing its two endpoints in phase space:
    sa = (0.0,0.5,0.0)   # (u,v,w) an event on the equator at ct=0.0
    sb = (1.0,1.0,0.6)   # (u,v,w) an event at the south pole at ct=0.9    

    steps = 5
    path = cva.solve.run(sa,sb,steps)
    cva.view.draw(path,title="Case 19: Sphere collapsing at 50\% light speed")

if __name__ == '__main__':
    case19_collapsing_sphere()
