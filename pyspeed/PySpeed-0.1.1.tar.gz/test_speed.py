#!/usr/bin/env python
import speed
for i in speed.progress(xrange(10000000)): pass

for i in speed.gprogress(xrange(5)):
    for j in speed.gprogress(xrange(10*500000)): pass


