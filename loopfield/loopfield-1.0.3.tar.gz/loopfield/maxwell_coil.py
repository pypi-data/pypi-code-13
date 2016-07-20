#!/usr/bin/env python3

import loopfield as lf
import loopfield.plot as lfp

# field object
field = lf.Field(length_units = lf.mm,
                 current_units = lf.A,
                 field_units = lf.uT)

# 49/64/49 Turn Maxwell coil on x-axis: measurements as-built


# center winding
min_r = 75./2
max_r = 88./2
min_z = -5.5/2
max_z = +5.5/2
n_r = 8
n_z = 8
for i in range(0, n_r):
  r = min_r + (max_r - min_r) * i / (n_r-1)
  for j in range(0, n_z):
    z = min_z + (max_z - min_z) * j / (n_z-1)
    c = lf.Loop([z, 0, 0], [1, 0, 0], r, 1)    
    field.addLoop(c)

# outer windings
min_r = 55./2
max_r = 63./2
min_z = 48./2
max_z = 56./2
n_r = 7
n_z = 7
for i in range(0, n_r):
  r = min_r + (max_r - min_r) * i / (n_r-1)
  for j in range(0, n_z):
    z = min_z + (max_z - min_z) * j / (n_z-1)
    c1 = lf.Loop([-z, 0, 0], [1, 0, 0], r, 1)    
    c2 = lf.Loop([+z, 0, 0], [1, 0, 0], r, 1)    
    field.addLoop(c1)
    field.addLoop(c2)


# evaluate field at center of coil
Bc = field.evaluate([0., 0., 0.])
print('Bc = ', Bc)

# function returns ratio of x-component to that at coil center
def x_ratio(B):
  return B[0] / Bc[0]

# create XY plot
min_x = -60
max_x = +60
min_y = -60
max_y = +60
n_x = 101
n_y = 101
plot = lfp.plotXY(field,
                  min_x, max_x, n_x,
                  min_y, max_y, n_y)

# add field lines
plot.fieldLines()

# add loop symbols
plot.loopSymbols(scale = 0.05)

# add 1% bound region
tol = 0.01
plot.region(x_ratio, [1.-tol, 1.+tol], color='red', alpha=0.5,
            label = ('Field error < %2.1f%%' % (100*tol)))

# add circled area
#center_r = 16
#plot.circle([0., 0.], radius = center_r, color='blue', alpha=0.5,
#            label = ('r = %2.1f mm' % center_r))

# add rectangular area
area_x = 12
area_y = 16
plot.rectangle([-area_x, +area_x, -area_y, +area_y],
               color='blue', alpha = 0.5,
               label = (' %2.1f x %2.1f mm' % (2*area_x, 2*area_y)))

# add text
plot.labels(title = '"40mm" 49/64/49-Turn Maxwell Coil\n(as-built measurements)',
            xlabel = 'x (mm)', ylabel = 'y (mm)')

# save plot
plot.save('maxwell_as_built.png')

