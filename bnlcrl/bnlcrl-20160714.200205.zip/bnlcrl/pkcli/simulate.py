from bnlcrl.crl_simulator import CRLSimulator, DEFAULTS_FILE
from bnlcrl.utils import console, convert_types, read_json
from pykern.pkdebug import pkdp, pkdc
import argh

@argh.arg('cart_ids', nargs='*')
# @argh.arg('energy', type=float)
def default_command(cart_ids, energy, optional=123):
    """Runner of the CRL simulator.

    Example of execution:

    $ python crl_console.py --cart_ids 2 4 6 7 8 --energy=21500 --p0=6.52

    "d","d_ideal","f","p0","p1","p1_ideal"
    0.000372455276869,-0.0669574652539,1.04864377922,6.52,1.24962754472,1.31695746525

    Args:
        cart_ids (list): list of cartridges ids.
        energy (float): photon energy [eV].
        optional (str): optional argument.
    """

    # args = console(CRLSimulator, DEFAULTS_FILE)
    # pkdp('args: {}', args)
    return {
        'cart_ids': cart_ids,
        'energy': energy,
    }

    '''
    defaults = convert_types(read_json(DEFAULTS_FILE)['parameters'])
    args = {}
    for key in defaults.keys():
        args[key] = defaults[key]['default']
    args['cart_ids'] = [cart_ids]
    args['energy'] = energy
    CRLSimulator(**args)
    '''
