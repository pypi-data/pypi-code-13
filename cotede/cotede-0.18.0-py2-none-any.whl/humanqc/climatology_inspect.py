# -*- coding: utf-8 -*-

"""

"""

import numpy as np
from numpy import ma
# from scipy.stats import norm, rayleigh, expon, halfnorm, exponpow, exponweib
from scipy.stats import exponweib
# from scipy.stats import kstest

from cotede.utils import ProfilesQCPandasCollection
from cotede.misc import combined_flag
from cotede.humanqc import HumanQC


def climatology_inspect(data, varname, flagname, featuresnames, niter=5):
    """
    """
    q = 0.90
    assert varname in data

    import pandas as pd
    #data['id'] = range(data.shape[0])
    #data.set_index('id', drop=True, inplace=True)

    if 'human_flag' not in data:
        data['human_flag'] = ma.masked_all(data[flagname].shape,
                dtype='object')
    data['flag_calibrating'] = data[flagname].copy()
    data.loc[data.human_flag == 'good', 'flag_calibrating'] = 1
    data.loc[data.human_flag == 'bad', 'flag_calibrating'] = 4

    #result = calibrate4flags(data['flag_calibrating'], data[featuresnames], q=q)

    #error_log = [{'err': result['n_err'],
    #    'err_ratio': result['err_ratio'],
    #    'p_optimal': result['p_optimal']}]

    #for i in range(12, 6, -1):
    for i in range(niter):

        data['outlier'] = (data['flag_calibrating'] <= 2) & (data[featuresnames] > 6)

        grp = data[data.outlier].groupby('profileid')
        profileids = grp[[featuresnames]].max().sort_values(featuresnames, ascending=False).index

        # In the future order by how badly AD mistaked
        if len(profileids) == 0:
            break
        # 5 random profiles with mistakes
        # for pid in profileids[:10]:
        #top_profileids = profileids[:int(profileids.shape[0]/2)]
        #for pid in np.random.permutation(top_profileids)[:5]:
        for pid in profileids:
            print("Profile: %s" % pid)
            profile = data[data.profileid == pid]
            try:
                clim = {'z': profile['PRES'],
                        'mn': profile['woa_mean'],
                        'std': profile['woa_std']
                        }
            except:
                clim = None

            print profile.loc[profile.human_flag.isnull(), featuresnames].max()
            h = HumanQC().eval(
                    profile[varname],
                    profile['PRES'],
                    baseflag=profile['flag_calibrating'],
                    #fails=np.array(profile['mistake']),
                    #fails=ma.array(profile.woa_normbias_abs == float(
                    #    profile.loc[profile.human_flag.isnull(),
                    #        featuresnames].max())),
                    fails=ma.array(profile.woa_normbias_abs > 6),
                    #fails=ma.array(profile.derr == profile.loc[
                    #    profile.human_flag.isnull(), 'woa_normbias_abs'].max()),
                    humanflag=ma.masked_values(
                        profile['human_flag'], None).astype('object'),
                    clim=clim)

            # Update human_flag only at the new values
            profile.loc[:, 'human_flag'] = h
            for i in profile.index[profile.human_flag.notnull()]:
                data.loc[i, 'human_flag'] = profile.loc[i, 'human_flag']

        data.loc[data.human_flag == 'good', 'flag_calibrating'] = 1
        data.loc[data.human_flag == 'bad', 'flag_calibrating'] = 4

    #result['human_flag'] = data['human_flag']

    return data['human_flag']
