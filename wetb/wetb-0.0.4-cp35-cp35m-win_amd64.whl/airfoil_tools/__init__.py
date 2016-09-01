import numpy as np
from scipy.interpolate import interp1d
def smoothen_LE(airfoil_x, airfoil_y, n=1000):
    LE_index = np.argmin(airfoil_x)
    assert airfoil_y[:LE_index].mean() > airfoil_y[LE_index:].mean()  # upper side first
    c4_upper_index = np.argmin(np.abs(airfoil_x[:LE_index] - .25))
    c4_lower_index = np.argmin(np.abs(airfoil_x[LE_index:] - .25)) + LE_index
    print (c4_upper_index, c4_lower_index, LE_index)
    f = interp1d(airfoil_y[c4_lower_index:c4_upper_index - 1:-1], airfoil_x[c4_lower_index:c4_upper_index - 1:-1], 'cubic')
    y = np.linspace(airfoil_y[c4_upper_index], airfoil_y[c4_lower_index], n)

    x = np.r_[airfoil_x[:c4_upper_index], f(y), airfoil_x[c4_lower_index:]]
    y = np.r_[airfoil_y[:c4_upper_index], y, airfoil_y[c4_lower_index:]]
    return x, y
