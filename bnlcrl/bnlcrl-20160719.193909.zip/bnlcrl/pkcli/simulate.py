# -*- coding: utf-8 -*-
u"""Utilities for X-Ray beamlines.

The module to perform the following operations:

- get the Index of Refraction (`Delta`) value;
- simulate Compound Refractive Lenses (CRL) in the approximation of thick lens.
"""
import argh

from bnlcrl.crl_simulator import CRLSimulator, DEFAULTS_FILE as DEFAULTS_FILE_CRL
from bnlcrl.delta_finder import DeltaFinder, DEFAULTS_FILE as DEFAULTS_FILE_DELTA
from bnlcrl.utils import convert_types, read_json

defaults_crl = convert_types(read_json(DEFAULTS_FILE_CRL)['parameters'])
defaults_delta = convert_types(read_json(DEFAULTS_FILE_DELTA)['parameters'])


@argh.arg('cart-ids', nargs='*', type=str)
@argh.arg('--lens-array', nargs='+', type=int)
@argh.arg('--r-array', nargs='+', type=float)
def simulate_crl(
        cart_ids,
        energy,
        beamline=defaults_crl['beamline']['default'],  # 'smi',
        calc_delta=defaults_crl['calc_delta']['default'],  # False,
        d_ssa_focus=defaults_crl['d_ssa_focus']['default'],  # 8.1,
        data_file=defaults_crl['data_file']['default'],  # 'Be_delta.dat',
        dl_cart=defaults_crl['dl_cart']['default'],  # 0.03,
        dl_lens=defaults_crl['dl_lens']['default'],  # 0.002,
        lens_array=defaults_crl['lens_array']['default'],  # [1, 2, 4, 8, 16],
        outfile=defaults_crl['outfile']['default'],  # False,
        output_format=defaults_crl['output_format']['default'],  # 'csv',
        p0=defaults_crl['p0']['default'],  # 6.2,
        verbose=defaults_crl['verbose']['default'],  # False,
        r_array=defaults_crl['r_array']['default'],  # [50.0, 200.0, 500.0],
        teta0=defaults_crl['teta0']['default'],  # 6e-05,
        use_numpy=defaults_crl['use_numpy']['default'],  # False,
):
    """Runner of the CRL simulator.

    Example::

        d = default_command(
            cart_ids=['2', '4', '6', '7', '8'],
            energy=21500,
            p0=6.52,
            verbose=True
        )

    Output::

        "d","d_ideal","f","p0","p1","p1_ideal"
        0.00120167289264,-0.0661303590822,1.0480597835,6.52,1.24879832711,1.31613035908

    Args:
        cart_ids (list): list of cartridges ids.
        energy (float): photon energy [eV].
        beamline (str): beamline name.
        calc_delta (bool): a flag to calculate delta analytically.
        d_ssa_focus (float): distance from secondary source aperture (SSA) [m].
        data_file (str): a *.dat data file in bnlcrl/package_data/dat/ directory with delta values for the material of the CRL (e.g., Be).
        dl_cart (float): distance between centers of two neighbouring cartridges [m].
        dl_lens (float): distance between two lenses within a cartridge [m].
        lens_array (list): list of possible number of lenses in cartridges.
        outfile (str): output file.
        output_format (str): output file format (CSV, JSON, plain text).
        p0 (float): distance from z=50.9 m to the first lens in the most upstream cartridge at the most upstream position of the transfocator [m].
        r_array (list): set of radii of available lenses in different cartridges [um].
        teta0 (float): divergence of the beam before CRL [rad].
        use_numpy (bool): a flag to use NumPy for operations with matrices.
        verbose (bool): a flag to print output to console.

    Returns:
        dict: dictionary with the resulted values of CRL parameters.
    """

    crl = CRLSimulator(
        cart_ids=cart_ids,
        energy=energy,
        beamline=beamline,
        calc_delta=calc_delta,
        d_ssa_focus=d_ssa_focus,
        data_file=data_file,
        dl_cart=dl_cart,
        dl_lens=dl_lens,
        lens_array=lens_array,
        outfile=outfile,
        output_format=output_format,
        p0=p0,
        verbose=verbose,
        r_array=r_array,
        teta0=teta0,
        use_numpy=use_numpy,
    )
    return {
        'd': crl.d,
        'd_ideal': crl.d_ideal,
        'f': crl.f,
        'p0': crl.p0,
        'p1': crl.p1,
        'p1_ideal': crl.p1_ideal,
    }


@argh.arg('energy', type=float)
def find_delta(
        energy,
        calc_delta=defaults_delta['calc_delta']['default'],
        characteristic=defaults_delta['characteristic']['default'],
        data_file=defaults_delta['data_file']['default'],
        e_max=defaults_delta['e_max']['default'],
        e_min=defaults_delta['e_min']['default'],
        e_step=defaults_delta['e_step']['default'],
        formula=defaults_delta['formula']['default'],
        n_points=defaults_delta['n_points']['default'],
        outfile=defaults_delta['outfile']['default'],
        precise=defaults_delta['precise']['default'],
        use_numpy=defaults_delta['use_numpy']['default'],
        verbose=defaults_delta['verbose']['default'],
):
    """Determine the Index of Refraction (delta).

    The index of refraction can be defined by three different methods/approaches:

        1) Get delta for the closest energy from the saved *.dat files (see bnlcrl/package_data/dat/).

        2) Get delta from http://henke.lbl.gov/optical_constants/getdb2.html.

        3) Calculate delta analytically (requires ``periodictable`` package installed).

    Args:
        energy (float): photon energy [eV].
        calc_delta (bool): a flag to calculate delta analytically.
        characteristic (str): characteristic to be extracted ('delta' or 'atten' for attenuation length).
        data_file (str): a *.dat data file in bnlcrl/package_data/dat/ directory with delta values for the material of the CRL (e.g., Be).
        e_max (float): the highest available energy [eV].
        e_min (float): the lowest available energy [eV].
        e_step (float): energy step size used for saving data to a file [eV].
        formula (str): material's formula of the interest.
        n_points (int): number of points to get from the server.
        outfile (str): optional output file.
        precise (bool): a flag to find delta within the energy interval +/- 1 eV from the specified energy.
        use_numpy (bool): a flag to use NumPy.
        verbose (bool): a flag to print output to console.

    Returns:
        dict: dictionary with the resulted delta.
    """
    delta = DeltaFinder(
        energy=energy,
        calc_delta=calc_delta,
        characteristic=characteristic,
        data_file=data_file,
        e_max=e_max,
        e_min=e_min,
        e_step=e_step,
        formula=formula,
        n_points=n_points,
        outfile=outfile,
        precise=precise,
        use_numpy=use_numpy,
        verbose=verbose,
    )
    return {
        'characteristic_value': delta.characteristic_value,
        'closest_energy': delta.closest_energy,
    }
