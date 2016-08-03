
import cotede.qc
from cotede.qc import ProfileQC
from cotede.qc import fProfileQC
from cotede.misc import combined_flag

import pdb; pdb.set_trace()
f = "/Users/castelao/.cotederc/data/dPIRX003.cnv"
f = "/Users/castelao/.cotederc/data/dPIRX010.cnv"
profile = cotede.qc.fProfileQC(f, cfg='cotede', saveauxiliary=True)
f = "/Users/castelao/.cotederc/data/TSG_PIR_001.cnv"
#f = '/Users/castelao/work/projects/python/cotede/data/piratadata/piratax/dPIRX014.cnv'
profile = cotede.qc.fProfileQC(f, cfg='tsg', saveauxiliary=True)

profile = cotede.qc.fProfileQC(f, cfg='anomaly_detection', saveauxiliary=True)

from cotede.anomaly_detection import *
datadir = '/Users/castelao/work/projects/python/cotede/data/piratadata/piratax'
#datadir = '/Users/castelao/work/projects/python/cotede/data/piratadata'
output = calibrate_anomaly_detection(datadir, 'TEMP', cfg='cotede')
print output.keys()
print output['n_misfit']
print output['p_optimal']
import pdb; pdb.set_trace()
human_calibrate_mistakes(datadir, 'TEMP', cfg='cotede', niter=5)

#print(f)
import pdb; pdb.set_trace()
from cotede.humanqc import HumanQC
hflag = HumanQC()
hflag.eval(profile['TEMP'], profile['PRES'])

import sys; sys.exit()
print("=========")
f = '/Users/castelao/work/projects/python/cotede/data/piratadata/piratai/dPIRA011.cnv'
#print(f)
p = cotede.qc.fProfileQC(f, cfg='anomaly_detection')

print("=========")
inputfiles = ['/Users/castelao/work/projects/python/cotede/test_data/dPIRX001.cnv',
        '/Users/castelao/work/projects/python/cotede/test_data/dPIRX002.cnv',
        '/Users/castelao/work/projects/python/cotede/test_data/dPIRX010.cnv.BAD']



print "outside!!!!!"
#for p in profiles:
#    print p.attributes['filename']

#inputdir = '/Users/castelao/work/projects/python/cotede/data/piratadata'
#inputdir = '/Users/castelao/work/projects/python/cotede/data/piratadata/piratax'
inputdir = '/Users/castelao/work/projects/python/cotede/test_data'

from cotede.utils import ProfilesQCPandasCollection
reload(cotede.qc); profiles = ProfilesQCPandasCollection(inputdir, saveauxiliary=True)#, timeout=15)

import pdb; pdb.set_trace()
