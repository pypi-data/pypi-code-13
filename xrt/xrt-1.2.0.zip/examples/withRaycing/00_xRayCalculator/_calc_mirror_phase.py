# -*- coding: utf-8 -*-
__author__ = "Konstantin Klementiev, Roman Chernikov"
__date__ = "22 Jan 2016"
import numpy as np
import matplotlib.pyplot as plt
# path to xrt:
import os, sys; sys.path.append(os.path.join('..', '..', '..'))  # analysis:ignore
import xrt.backends.raycing.materials as rm

L = 500.
pitch = 4e-3
p = 25000.
y = np.array([-1, 1]) * L/2.
dtheta = np.arctan2(y*np.sin(pitch), p + y*np.cos(pitch))

#stripe = rm.Material('Be', rho=1.848)
#stripe = rm.Material('C', rho=3.52)
#stripe = rm.Material(('Si', 'O'), quantities=(1, 2), rho=2.2)
#stripe = rm.Material('Si', rho=2.33)
#stripe = rm.Material('Al', rho=2.7)
#stripe = rm.Material('Ni', rho=8.9)
#stripe = rm.Material('Pb', rho=11.35)
#stripe = rm.Material('Au', rho=19.3)

#E = np.logspace(1 + np.log10(3), 4 + np.log10(5), 501)
E = np.logspace(3, 4, 501)

stripe = rm.Material('Si', rho=2.33)
rsL, rpL = stripe.get_amplitude(E, np.sin(pitch+dtheta[0]))[0:2]
rsH, rpH = stripe.get_amplitude(E, np.sin(pitch+dtheta[-1]))[0:2]
phs = np.angle(rsH) - np.angle(rsL)
php = np.angle(rpH) - np.angle(rpL)
plt.semilogx(E, phs, 'r', label=stripe.name)

stripe = rm.Material('Au', rho=2.33)
rsL, rpL = stripe.get_amplitude(E, np.sin(pitch+dtheta[0]))[0:2]
rsH, rpH = stripe.get_amplitude(E, np.sin(pitch+dtheta[-1]))[0:2]
phs = np.angle(rsH) - np.angle(rsL)
php = np.angle(rpH) - np.angle(rpL)
plt.semilogx(E, phs, 'b', label=stripe.name)

plt.legend(loc='lower left')

plt.gca().set_xlim(E[0], E[-1])
plt.show()
