# -*- coding: utf-8 -*-
u"""Utilities for X-Ray beamlines.

The module to perform the following operations:

- get the Index of Refraction (`Delta`) value;
- simulate Compound Refractive Lenses (CRL) in the approximation of thick lens.
"""
from bnlcrl.crl_simulator import CRLSimulator, DEFAULTS_FILE
from bnlcrl.utils import console, convert_types, read_json
from pykern.pkdebug import pkdp, pkdc
import argh


@argh.arg('cart_ids', nargs='*', type=str)
@argh.arg('--lens-array', nargs='+', type=int)
@argh.arg('--r-array', nargs='+', type=float)
def default_command(
        cart_ids,
        energy,
        beamline='smi',
        calc_delta=False,
        d_ssa_focus=8.1,
        data_file='Be_delta.dat',
        dl_cart=0.03,
        dl_lens=0.002,
        lens_array=[1, 2, 4, 8, 16],
        outfile=False,
        output_format='csv',
        p0=6.2,
        quiet=False,
        r_array=[50.0, 200.0, 500.0],
        teta0=6e-05,
        use_numpy=False,
):
    """Runner of the CRL simulator.

    Example::

        d = default_command(
            cart_ids=(2, 4, 6, 7, 8),
            energy=21500,
            p0=6.52
        )

    Output::

        "d","d_ideal","f","p0","p1","p1_ideal"
        0.000372455276869,-0.0669574652539,1.04864377922,6.52,1.24962754472,1.31695746525

    Args:
        cart_ids (list): list of cartridges ids.
        energy (float): photon energy [eV].
        beamline (str): beamline name.
        calc_delta (bool): calculate delta analytically.
        d_ssa_focus (float): distance from secondary source aperture (SSA) [m].
        data_file (str): data file with delta values for the material of the CRL (e.g., Be).
        dl_cart (float): distance between centers of two neighbouring cartridges [m].
        dl_lens (float): distance between two lenses within a cartridge [m].
        lens_array (list): list of possible number of lenses in cartridges.
        outfile (str): output file.
        output_format (str): output file format (CSV, JSON, plain text).
        p0 (float): distance from z=50.9 m to the first lens in the most upstream cartridge at the most upstream position of the transfocator [m].
        quiet (bool): suppress output to console.
        r_array (list): set of radii of available lenses in different cartridges [um].
        teta0 (float): divergence of the beam before CRL [rad].
        use_numpy (bool): use NumPy for operations with matrices.

    Returns:
        dict: dictionary with the resulted values of CRL parameters.
    """

    '''
    defaults = convert_types(read_json(DEFAULTS_FILE)['parameters'])
    args = {}
    for key in defaults.keys():
        args[key] = defaults[key]['default']
    args['cart_ids'] = [cart_ids]
    args['energy'] = energy
    CRLSimulator(**args)
    '''

    return {
        'cart_ids': cart_ids,
        'energy': energy,
        'lens_array': lens_array,
    }
