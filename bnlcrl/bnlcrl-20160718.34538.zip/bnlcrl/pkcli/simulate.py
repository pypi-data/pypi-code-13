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

defaults = convert_types(read_json(DEFAULTS_FILE)['parameters'])


@argh.arg('cart-ids', nargs='*', type=str)
@argh.arg('--lens-array', nargs='+', type=int)
@argh.arg('--r-array', nargs='+', type=float)
def default_command(
        cart_ids,
        energy,
        beamline=defaults['beamline']['default'],  # 'smi',
        calc_delta=defaults['calc_delta']['default'],  # False,
        d_ssa_focus=defaults['d_ssa_focus']['default'],  # 8.1,
        data_file=defaults['data_file']['default'],  # 'Be_delta.dat',
        dl_cart=defaults['dl_cart']['default'],  # 0.03,
        dl_lens=defaults['dl_lens']['default'],  # 0.002,
        lens_array=defaults['lens_array']['default'],  # [1, 2, 4, 8, 16],
        outfile=defaults['outfile']['default'],  # False,
        output_format=defaults['output_format']['default'],  # 'csv',
        p0=defaults['p0']['default'],  # 6.2,
        verbose=defaults['verbose']['default'],  # False,
        r_array=defaults['r_array']['default'],  # [50.0, 200.0, 500.0],
        teta0=defaults['teta0']['default'],  # 6e-05,
        use_numpy=defaults['use_numpy']['default'],  # False,
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
        verbose (bool): print output to console.
        r_array (list): set of radii of available lenses in different cartridges [um].
        teta0 (float): divergence of the beam before CRL [rad].
        use_numpy (bool): use NumPy for operations with matrices.

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
