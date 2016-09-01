"""Example of fitting Mann parameters to a "series" of a turbulence box"""
import numpy as np
from wetb.wind.turbulence.mann_parameters import fit_mann_model_spectra, \
    plot_mann_spectra
from wetb.wind.turbulence.turbulence_spectra import spectra

#nx = 4096
#l = nx * 1.758
#ny, nz = 32, 32
#sf = (nx / l)
#u, v, w = [np.fromfile(r"C:\mmpe\HAWC2\models\DTU10MWRef6.0\turb\l30.0_ae1.00_g3.9_h1_4096x32x32_1.758x5.62x5.62_s0002%s.turb" % uvw, np.dtype('<f'), -1).reshape(nx , ny * nz) for uvw in ['u', 'v', 'w']]
#ae, L, G = fit_mann_model_spectra(*spectra(sf, u, v, w))
#print (ae, L, G)


import matplotlib.pyplot as plt
plot_mann_spectra(1, 30, 0, u_ref=10, plt=plt, spectra=["uu"], style='--')
plot_mann_spectra(1, 200, 0, u_ref=10, plt=plt, spectra=['uu'], style=':')
plot_mann_spectra(1, 30, 3.9, u_ref=10, plt=plt, spectra=["uu"], style='-.')
plot_mann_spectra(1, 200, 3.9, u_ref=10, plt=plt, spectra=['uu'])

plt.show()
