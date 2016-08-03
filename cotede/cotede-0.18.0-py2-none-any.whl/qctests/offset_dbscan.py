# -*- coding: utf-8 -*-

"""

"""

#import numpy as np
#from numpy import ma


def density_inversion(data, cfg, saveaux=False):
    """

        Must decide where to set the flags.
    """
    assert ('TEMP' in data.keys()), \
            "Missing TEMP"
    assert ('PSAL' in data.keys()), \
            "Missing PSAL"
    assert ('PRES' in data.keys()), \
            "Missing PRES"

    ds = densitystep(data['TEMP'], data['PSAL'],
            data['PRES'])

    if ds is None:
        # FIXME:
        print("Improve error handling. Package gsw is not available")
        return

    flag = np.zeros(ds.shape, dtype='i1')

    flag[np.nonzero(ds >= cfg['threshold'])] = cfg['flag_good']
    flag[np.nonzero(ds < cfg['threshold'])] = cfg['flag_bad']

    # Flag as 9 any masked input value
    #for v in ['TEMP', 'PSAL', 'PRES']:
    #    flag[ma.getmaskarray(data[v])] = 9

    if saveaux:
        return flag, ds
    else:
        return flag
