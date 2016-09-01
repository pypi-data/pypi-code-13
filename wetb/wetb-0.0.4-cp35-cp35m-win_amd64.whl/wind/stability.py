'''
Created on 05/10/2015

@author: MMPE
'''
from wetb.wind.turbulence import spectrum
import numpy as np
from scipy.integrate import trapz

def MoninObukhov_length(u_ref, w, T, specific_humidity=None):
    """Calculate the Monin Obukhov length

    Not validated!!!

    parameters
    ----------
    u_ref :
        Refencence velocity at hub height
    w : array_like
        Vertical wind fluctuations
    T : array_like
        Temperature in celcius
    """
    K = 0.4
    g = 9.82
    if specific_humidity is not None:
        potential_temperature = (w * (T + 273.15)).mean() + 0.61 * (T + 273.15).mean() * (w * specific_humidity).mean()
    else:
        potential_temperature = (w * (T + 273.15)).mean()
    return -u_ref ** 3 * (T.mean() + 273.15) / (K * g * potential_temperature)



def humidity_relative2specific(relative_humidity, T, P):
    """Not validated
    parameters
    ----------
    relative_humidity : float
        Relative humidity [%]
    T : float
        Temperature [C]
    P : float
        Barometric pressure [Pa]
    """
    return relative_humidity * np.exp(17.67 * T / (T + 273.15 - 29.65)) / 0.263 / P

def humidity_specific2relative2(specific_humidity, T, P):
    """Not validated
    parameters
    ----------
    specific_humidity : float
        specific_humidity [kg/kg]
    T : float
        Temperature [C]
    P : float
        Barometric pressure [Pa]
    """
    return 0.263 * P * specific_humidity / np.exp(17.67 * T / (T + 273.15 - 29.65))

if __name__ == "__main__":
    print (humidity_relative2specific(85, 8, 101325))
    print (humidity_specific2relative2(5.61, 8, 101325))
