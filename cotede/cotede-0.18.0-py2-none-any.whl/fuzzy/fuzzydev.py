
import skfuzzy as fuzz

from cotede.qc import fProfileQC

import cotede.qc

#f = "/Users/castelao/Dropbox/Public/argo/20150127_prof.nc"
#from argo import argo
#from cotede.qc import ProfileQC
#profile = argo.extract_profile(f)[0]

cfg = {
        "output": {
            "low": [0.0, 0.225, 0.45],
            "medium": [0.275, 0.5, 0.725],
            "high": [0.55, 0.775, 1.0]
            },
        "features": {
            "spike": {
                "weight": 1,
                "low": {
                    "coef": [-1e30, -1e30, 0.07, 0.2]
                    },
                "medium": {
                    "coef": [0.07, 0.2, 2, 6]
                    },
                "high": {
                    [2, 6, 1e30, 1e30]
                    }
                },
            "woa_relbias": {
                "weight": 1,
                "low": {
                    "coef": [-1e30, -1e30, 3, 4]
                    },
                "medium": {
                    "coef": [3, 4, 5, 6]
                    },
                "high": {
                    "coef": [5, 6, 1e30, 1e30]
                    }
                },
            "gradient": {
                "weight": 1,
                "low": {
                    "coef": [-1e30, -1e30, 0.5, 1.5]

                    "coef": [0.5, 1.5, 3, 4]
                    },
                "high": {
                    "coef": [3, 4, 1e30, 1e30]
                    }
                }
            }
        }

del(cfg['features']['woa_relbias'])

datadir = '/Users/castelao/work/projects/python/cotede/data/piratadata/piratax'

from cotede.utils import ProfilesQCPandasCollection
db = ProfilesQCPandasCollection(datadir, cfg='cotede', saveauxiliary=True)

features = db.auxiliary['TEMP'].loc[:, ['gradient', 'spike']]
features['flag'] = cotede.misc.combined_flag(db.flags['TEMP'])

# Remove flags 9.
features = features[features.flag != 9]
# Remove lines with any Nan
features = features.dropna(how='any')

from cotede.fuzzy import fuzz

def cost(p):
    cfg = {"output": {
        "low": [0.0, 0.225, 0.45],
        "medium": [0.275, 0.5, 0.725],
        "high": [0.55, 0.775, 1.0]
        },'features': {'gradient': {}, 'spike': {}}}
    cfg['features']['gradient']['low'] = \
            [p[1]-0.75-1, p[1]-0.75]
    cfg['features']['gradient']['medium'] = \
            [p[1]-0.75-1, p[1]-0.75, p[1]+0.75, p[1]+0.75+1]
    cfg['features']['gradient']['high'] = \
            [p[1]+0.75, p[1]+0.75+1]

    cfg['features']['spike']['low'] = \
            [0.07, 0.2]
    cfg['features']['spike']['medium'] = \
            [p[2]-0.9-0.13, p[2]-0.9, p[2]+0.9, p[2]+0.9+4]
    cfg['features']['spike']['high'] = \
            [p[2]+0.9, p[2]+0.9+4]

    fz = fuzz(features, cfg)

    ind = ((fz < p[0]) & (np.array(features.flag) >= 3)) | \
            ((fz > p[0]) & (np.array(features.flag) <= 2))

    error = np.absolute(fz[ind] - p[0]).sum()

    #fpositive = features.loc[(fz<p[0]) & (features.flag >= 3)].size
    #fnegative = features.loc[(fz>p[0]) & (features.flag <= 2)].size
    #error = fpositive + fnegative

    return error

from scipy import optimize
p0 = (0.4, 2.25, 1.1)
optimize.fmin_tnc(cost, p0)


p = {'gradient': {'low': [1, 0.5], 'high': [3.5, 0.5]},
        'spike': {'low': [.135, 0.065], 'high': [4, 2]}
        }

f = '/Users/castelao/work/projects/python/cotede/data/piratadata/piratax/dPIRX027.cnv'
f = '/Users/castelao/.cotederc/data/PIRA001.cnv'
f = '/Users/castelao/.cotederc/data/dPIRX010.cnv'
#f = '/Users/castelao/.cotederc/data/PIRA001.cnv'
#print(f)
import pdb; pdb.set_trace()
profile = cotede.qc.fProfileQC(f, cfg='fuzzy', saveauxiliary=True)
import sys; sys.exit()
from cotede.humanqc import HumanQC
#hflag = HumanQC().eval(profile['temperature'], profile['pressure'])
#import pdb; pdb.set_trace()
print("=========")
f = '/Users/castelao/work/projects/python/cotede/data/piratadata/piratai/dPIRA011.cnv'
#print(f)
p = cotede.qc.fProfileQC(f)

print("=========")
inputfiles = ['/Users/castelao/work/projects/python/cotede/test_data/dPIRX001.cnv',
        '/Users/castelao/work/projects/python/cotede/test_data/dPIRX002.cnv',
        '/Users/castelao/work/projects/python/cotede/test_data/dPIRX010.cnv.BAD']

print("== Running Serial ==")
#reload(cotede.qc); profiles = cotede.utils.profilescollection.process_profiles_serial(inputfiles, saveauxiliary=False)
print("== Running Parallel ==")
#reload(cotede.qc); profiles = cotede.utils.profilescollection.process_profiles(inputfiles, saveauxiliary=False, timeout=15)


print "outside!!!!!"
#for p in profiles:
#    print p.attributes['filename']

#inputdir = '/Users/castelao/work/projects/python/cotede/data/piratadata'
#inputdir = '/Users/castelao/work/projects/python/cotede/data/piratadata/piratax'
inputdir = '/Users/castelao/work/projects/python/cotede/test_data'

from cotede.utils import ProfilesQCPandasCollection
reload(cotede.qc); profiles = ProfilesQCPandasCollection(inputdir, saveauxiliary=True)#, timeout=15)

import pdb; pdb.set_trace()
