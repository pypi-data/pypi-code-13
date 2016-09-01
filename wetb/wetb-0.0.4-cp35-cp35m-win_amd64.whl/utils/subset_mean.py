'''
Created on 24/06/2016

@author: MMPE
'''

import numpy as np
import unittest
from wetb.utils.geometry import rpm2rads


def power_mean(power, trigger_indexes, I, rotor_speed, time, air_density=1.225, rotor_speed_mean_samples=1) :
    """Calculate the density normalized mean power, taking acceleration of the rotor into account

    Parameters
    ---------
    Power : array_like
        Power [W]
    trigger_indexes : array_like
        Trigger indexes
    I : float
        Rotor inerti [kg m^2]
    rotor_speed : array_like
        Rotor speed [rad/s]
    time : array_like
        time [s]
    air_density : int, float or array_like, optional
        Air density.
    rotor_speed_mean_samples : int
        To reduce the effect of noise, the mean of a number of rotor speed samples can be used

    Returns
    -------
    mean power including power used to (de)accelerate rotor

    Examples:
    ---------
    turbine_power_mean = lambda power, triggers : power_mean(power, triggers, I=2.5E7, rot_speed, time, rho)
    trigger_indexes = time_trigger(time,30)
    wsp_mean, power_mean = subset_mean([wsp, power],trigger_indexes,mean_func={1:turbine_power_mean})
    """
    if rotor_speed_mean_samples == 1:
        rs1 = rotor_speed[trigger_indexes[:-1]]
        rs2 = rotor_speed[trigger_indexes[1:] - 1]
    else:
        rs = np.array([rotor_speed[max(i - rotor_speed_mean_samples, 0):i - 1 + rotor_speed_mean_samples].mean() for i in trigger_indexes])
        rs1 = rs[:-1]
        rs2 = rs[1:]


    power = np.array([np.nanmean(power[i1:i2], 0) for i1, i2 in zip(trigger_indexes[:-1].tolist(), trigger_indexes[1:].tolist())])
    if isinstance(air_density, (int, float)):
        if air_density != 1.225:
            power = power / air_density * 1.225
    else:
        air_density = np.array([np.nanmean(air_density[i1:i2], 0) for i1, i2 in zip(trigger_indexes[:-1].tolist(), trigger_indexes[1:].tolist())])
        power = power / air_density * 1.225
    return power + 1 / 2 * I * (rs2 ** 2 - rs1 ** 2) / (time[trigger_indexes[1:] - 1] - time[trigger_indexes[:-1]])

def power_mean_func_kW(I, rotor_speed, time, air_density=1.225, rotor_speed_mean_samples=1) :
    """Return a power mean function [kW] used to Calculate the density normalized mean power, taking acceleration of the rotor into account

    Parameters
    ---------
    I : float
        Rotor inerti [kg m^2]
    rotor_speed : array_like
        Rotor speed [rad/s]
    time : array_like
        time [s]
    air_density : int, float or array_like, optional
        Air density.
    rotor_speed_mean_samples : int
        To reduce the effect of noise, the mean of a number of rotor speed samples can be used

    Returns
    -------
    mean power function

    Examples:
    ---------
    turbine_power_mean = power_mean_func_kW(power, triggers, I=2.5E7, rot_speed, time, rho)
    trigger_indexes = time_trigger(time,30)
    wsp_mean, power_mean = subset_mean([wsp, power],trigger_indexes,mean_func={1:turbine_power_mean})
    """
    def mean_power(power, trigger_indexes):
        return power_mean(power * 1000, trigger_indexes, I, rotor_speed, time , air_density, rotor_speed_mean_samples) / 1000
    return mean_power


def subset_mean(data, trigger_indexes, mean_func={}):
    if isinstance(data, list):
        data = np.array(data).T
    steps = np.diff(trigger_indexes)

    if np.all(steps == steps[0]):
        #equal distance
        subset_mean = np.nanmean(data[trigger_indexes[0]:trigger_indexes[-1]].reshape([ len(trigger_indexes) - 1, steps[0], data.shape[1]]), 1)
    else:
        subset_mean = np.array([np.nanmean(data[i1:i2], 0) for i1, i2 in zip(trigger_indexes[:-1].tolist(), trigger_indexes[1:].tolist())])
    for index, func in mean_func.items():
        att = data[:, index]
        subset_mean[:, index] = func(att, trigger_indexes)
    return subset_mean


def cycle_trigger(values, trigger_value=None, step=1, ascending=True, tolerance=0):
    if trigger_value is None:
        r = values.max() - values.min()
        values = (values[:] - r / 2) % r
        trigger_value = r / 2
    if ascending:
        return np.where((values[1:] > trigger_value + tolerance) & (values[:-1] <= trigger_value - tolerance))[0][::step]
    else:
        return np.where((values[1:] < trigger_value - tolerance) & (values[:-1] >= trigger_value + tolerance))[0][::step]


def time_trigger(time, step, start=None, stop=None):
    if start is None:
        start = time[0]
    time = np.round(time - start, 4)


    steps = np.round(np.diff(time), 4)
    if np.all(steps == steps[0]):
        # equal time step
        time = np.r_[time, time[-1] + steps[0]]
    if stop is None:
        stop = time[-1]
    else:
        stop -= start
    return np.where((time % step == 0) & (time >= 0) & (time <= stop))[0]




