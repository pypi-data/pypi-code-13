import numpy as np
from wetb.gtsdf import gtsdf
from wetb.utils.geometry import wsp_dir2uv
from wetb.wind.turbulence.turbulence_spectra import spectra
from wetb.wind.turbulence.mann_parameters import fit_mann_model_spectra


if __name__ == "__main__":
    """Example of fitting Mann parameters to a time series"""
    _, data, _ = gtsdf.load('unit_test/test_files/wspdataset.hdf5')
    f = 35
    u, v = wsp_dir2uv(data[:, 0], data[:, 2])

    u_ref = np.mean(u)
    u -= u_ref

    sf = f / u_ref
    ae, L, G = fit_mann_model_spectra(*spectra(sf, u, v))
    print (ae, L, G)


    """Example of fitting Mann parameters to a "series" of a turbulence box"""
    l = 65536
    nx = 16384
    ny, nz = 8, 8
    sf = (nx / l)
    u, v, w = [np.fromfile("unit_test/test_files/h2a16384_8_8_65536_32_32_0.15_40_3.3%s.dat" % uvw, np.dtype('<f'), -1).reshape(nx , ny * nz) for uvw in ['u', 'v', 'w']]
    ae, L, G = fit_mann_model_spectra(*spectra(sf, u, v, w))
    print (ae, L, G)
