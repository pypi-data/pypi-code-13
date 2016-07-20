#!/usr/bin/env python3

import time
import numpy as np
import _loopfield as lf

# create empty field with specified units
field = lf.Field(length_units = lf.cm,
                 current_units = lf.A,
                 field_units = lf.uT)

# single-turn 10 cm x-oriented coil at origin
position = [-5., 0., 0.]
normal = [1., 0., 0.]
radius = 10.
current = 1.
c = lf.Loop(position, normal, radius, current)
c1 = lf.Loop([5,0,0], normal, radius, current)

# add loop to field
field.addLoop(c);
field.addLoop(c1);
field.addLoop(c1);
field.addLoop(c1);

# evaluate vector field at origin
N = 1000000
pts = 100-200*np.random.random_sample((N, 3))

start_time = time.time()
B = field.evaluate(pts)
end_time = time.time()
print(str(N/(end_time - start_time)), ' pts/s')

#print('B = ', B)

