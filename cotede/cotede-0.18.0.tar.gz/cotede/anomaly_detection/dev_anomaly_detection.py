
import os
import shutil
import tempfile

from matplotlib import pyplot as plt
from seabird.cnv import fCNV

from cotede.utils import ProfilesQCPandasCollection
from cotede.utils.supportdata import download_testdata
from cotede.anomaly_detection import rank_files
from cotede.anomaly_detection import calibrate4flags



datalist = ["dPIRX010.cnv", "PIRA001.cnv", "dPIRX003.cnv"]
INPUTFILES = [download_testdata(f) for f in datalist]


varname = 'TEMP'
try:
    tmpdir = tempfile.mkdtemp()
    for f in INPUTFILES:
        shutil.copy(f, tmpdir)

    db = ProfilesQCPandasCollection(tmpdir, cfg='cotede',
            saveauxiliary=True)
    calibration_output = calibrate4flags(flags=db.flags[varname],
            features=db.auxiliary[varname], q=0.90)
finally:
    shutil.rmtree(tmpdir)


clim = db.auxiliary['TEMP']['woa_relbias']
clim = clim[clim < 10]

try:
    tmpdir = tempfile.mkdtemp()
    print("Created temporary directory: %s" % tmpdir)
    for f in INPUTFILES:
        shutil.copy(f, tmpdir)

    rank_list = rank_files(tmpdir, 'TEMP', cfg='cotede')

    p1 = fCNV(os.path.join(tmpdir, rank_list[0]))
    p2 = fCNV(os.path.join(tmpdir, rank_list[-1]))
finally:
    print("Deleting: %s" % tmpdir)
    shutil.rmtree(tmpdir)


print rank_list

plt.subplot(121)
plt.plot(p1['TEMP'], -p1['PRES'], '.')
plt.title(rank_list[0])
plt.subplot(122)
plt.plot(p2['TEMP'], -p2['PRES'], '.')
plt.xlim([26.8, 27.3])
plt.title(rank_list[-1])
plt.show()




import numpy as np
from numpy import ma
import pylab

#from scipy.stats import kstest

import cotede.qc
import cotede.utils
from cotede.misc import combined_flag
#from cotede.anomaly_detection import adjust_anomaly_coefficients

#from numpy import linspace
#from pylab import plot,show,hist,figure,title

#from cotede.misc import make_qc_index, split_data_groups, fit_tests, estimate_anomaly
from cotede.humanqc import HumanQC

# ============================================================================
# Variable to be analysec
#v = 'PSAL'
v = 'TEMP'
# Data that will be allways wrong
#hardlimit_flags = ['global_range']
# Dataset directory
inputdir = '/Users/castelao/work/projects/python/cotede/data/piratadata'
#inputdir = '/Users/castelao/work/projects/python/cotede/data/piratadata/piratax'
q=.90


# == Load the database ================================================
from cotede.utils import ProfilesQCPandasCollection
db = ProfilesQCPandasCollection(inputdir, cfg='cotede', saveauxiliary=True)
#aux = db.auxiliary[v]

from cotede.anomaly_detection import calibrate_anomaly_detection
out = calibrate_anomaly_detection(inputdir, v, cfg='eurogoos')


from cotede.anomaly_detection import *
#output = human_calibrate_mistakes(inputdir, 'TEMP', cfg='cotede', niter=10)
output = human_calibrate_mistakes(inputdir, 'TEMP', cfg='gtspp', niter=10)

import pdb; pdb.set_trace()
import sys; sys.exit()
import pdb; pdb.set_trace()


# ==== Reproducing the traditional tests =====================================
result = adjust_anomaly_coefficients(ind_qc, qctests, aux)

# ============================================================================
# To evaluate all profiles
db.flags[v]['humaneval'] = None
#db.flags[v]['humaneval'] = db.flags[v]['humaneval'].astype('bool')
# ----
for pid in db.data.profileid.unique()[:4]:
    ind_p = np.array(db.data.profileid == pid) #db.data.profileid.iloc[0]
    h = cotede.humanqc.HumanQC(
            np.array(db.data['TEMP'][ind_p]),
            np.array(db.data['pressure'][ind_p]),
            baseflag=ind_qc[ind_p])
    for i in np.nonzero(ma.getmaskarray(h.humanflag)==False)[0]:
        db.flags[v]['humaneval'].iloc[np.nonzero(ind_p)[0][i]] = \
                h.humanflag[i]
# ============================================================================
import pdb; pdb.set_trace()

import pandas as pd
output = pd.DataFrame({'profileid': db.flags[v].profileid,
    'pressure': db.data.pressure,
    'TEMP': db.data[v],
    'humaneval': db.flags[v]['humaneval']})

filename = "guiteste"
store = pd.HDFStore(filename)
#output.to_hdf("%s_humaneval.hdf" % filename, 'df')
store.append('humaneval', output)

#import cotede.humaneval
#x = cotede.humaneval.HumanTrainning(v, inputdir, qctests, reference_flags)

niter = 5
# ==== Human eval
from numpy.random import permutation
from cotede.humaneval import HumanQC


data = {}
data['x'] = db.data['TEMP'].copy()
data['z'] = db.data['pressure'].copy()
data['profileid'] = db.data['profileid'].copy()

aux = db.auxiliary[v].copy()


def human_calibrate_mistakes(data, ind_qc_reference, aux, qctests=None,
        niter=5):
    if qctests is None:
        qctests = list(aux.keys())

    ind_humanqc = ind_qc_reference.copy()

    result = adjust_anomaly_coefficients(ind_humanqc, qctests, aux)
    error_log = [{'err': result['err'], 'err_ratio': result['err_ratio'],
        'p_optimal': result['p_optimal']}]

    for i in range(niter):
        # Profiles with any failure
        mistakes = (result['false_positive'] | result['false_negative'])
        profileids = data['profileid'][mistakes].unique()
        #ind = np.nonzero(ind_humanqc==False)
        #profileids = np.unique(db.data.profileid)
        #ind = np.nonzero([(db.data.profileid == p) & (ind_humanqc==True)][0])
        if len(profileids) == 0:
            break
        for pid in profileids[permutation(len(profileids))[:5]]:
            print("Profile: %s" % pid)
            ind_p = np.array(db.data.profileid == pid)
            print db.data.profilename[ind_p].iloc[0]
            mistakes = (result['false_positive'][ind_p] | 
                    result['false_negative'][ind_p])
            h = cotede.humaneval.HumanQC(
                    np.array(data['x'][ind_p]),
                    np.array(data['z'][ind_p]),
                    baseflag=ind_humanqc[ind_p],
                    fails=mistakes)#, doubt = ind_doubt[ind])
            for i in np.nonzero(ma.getmaskarray(h.humanflag)==False)[0]:
                if h.humanflag[i] == 'good':
                    ind_humanqc[np.nonzero(ind_p)[0][i]] = True
                elif h.humanflag[i] == 'bad':
                    ind_humanqc[np.nonzero(ind_p)[0][i]] = False
                elif h.humanflag[i] == 'doubt':
                    ind_humanqc.mask[np.nonzero(ind_p)[0][i]] = True
                    #ind_humanqc.mask[np.nonzero(ind)[0][i]] = np.nan

            result = adjust_anomaly_coefficients(ind_humanqc, qctests, aux)
            error_log.append({'err': result['err'],
                'err_ratio': result['err_ratio'],
                'p_optimal': result['p_optimal']})
        print error_log[-2]
        print error_log[-1]
    return {'ind_humanqc':ind_humanqc,
            'error_log': error_log,
            'result': result}


# ============================================================================
#h_ind = to_hdf("%s_humaneval.hdf" % filename, 'df')
h_map = pd.read_hdf('gui_humaneval.hdf', 'df')

ind_humanqc = make_qc_index(db.flags[v], ['global_range', 'gradient_depthconditional', 'spike_depthconditional', 'digit_roll_over', 'humaneval'])

db.data[v][ind_rangeqc==True].describe()
db.data[v][ind_pconditionalqc==True].describe()
db.data[v][ind_humanqc==True].describe()



profileids = db.data.profileid[false_negative].unique()
for pid in profileids:
    db.data[(db.data.profileid == pid) & false_negative]
    ind = db.data.profileid == pid #db.data.profileid.iloc[0]
    x = cotede.humaneval.HumanQC(db.data['TEMP'][ind], db.data['pressure'][ind], baseflags = ind_pconditionalqc[ind])
    for i in x.hbad_ind:
        ind_humanqc.iloc[np.nonzero(ind)[0][i]] = False
    for i in x.hgood_ind:
        db.flags[v]['humaneval'].iloc[np.nonzero(ind)[0][i]] = True
# ============================================================================
# ==== Estimate the PDF parameters ===========================================
#output = {}
#for teste in qctests:
#    max_good = (db.auxiliary[v][teste][db.flags[v][teste]==True]).max()
#    min_bad = (db.auxiliary[v][teste][db.flags[v][teste]==False]).min()

# ==== Estimate the probability of all the observations ======================
# ============================================================================

print "All data: %s" % ind.size
print "Out of range:"
print "Good data: %s" % ind[ind==True].size
print "Bad data: %s" % ind[ind==False].size
print "Percentage of bad data: %s" % (float(ind[ind==False].size) / ind[ind==True].size)







pylab.subplot(211)
hist(prob[false_negative])
pylab.title('False Negative')
pylab.subplot(212)
hist(prob[false_positive])
pylab.title('False Positive')
pylab.show()



db.data.profileid[false_positive].unique()
db.data.profileid[false_negative].unique()



#ind = (db.data.profileid == 0) & (false_positive == True)
#pylab.plot(db.data[v][ind], -db.data.pressure[ind], '.')
#ind = (db.data.profileid == 0) & (false_positive == False)
#pylab.plot(db.data[v][ind], -db.data.pressure[ind], 'r^')
#pylab.show()
#
#
#ind = (db_finite['profileid'] == 0) & (false_positive == True)
#pylab.plot(prob[ind], -db_finite['pressure'][ind], '.')
#pylab.show()


for pid in db.data.profileid.unique():
    ind = db.data.profileid == pid
    ind_good = ind & (ind_qc == True)
    ind_bad = ind & (ind_qc == False)
    ind_falneg = ind & (prob < p_optimal) & (ind_qc == True)
    ind_falpos = ind & (prob > p_optimal) & (ind_qc == False) & \
            (ind_rangeqc == True)
    pylab.plot(db.data[v][ind_good], -db.data.pressure[ind_good])
    pylab.plot(db.data[v][ind_good], -db.data.pressure[ind_good], 'b.')
    pylab.plot(db.data[v][ind_bad], -db.data.pressure[ind_bad], 'bx')
    pylab.plot(db.data[v][ind_falneg], -db.data.pressure[ind_falneg], 'r^')
    pylab.plot(db.data[v][ind_falpos], -db.data.pressure[ind_falpos], 'gs')
    pylab.title("Profile: %s" % pid)
    pylab.show()







samp = cruise.auxiliary['TEMP']['step'][ind_basicqc].compressed()

# picking 150 of from a normal distrubution
# with mean 0 and standard deviation 1
samp = norm.rvs(loc=0,scale=1,size=150) 
samp = cruise['TEMP'].compressed()

from seabird.cnv import fCNV
d = fCNV('/Users/castelao/Dropbox/working/cotede/data/piratadata/piratax/dPIRX003.cnv')
import cotede.qc
p = cotede.qc.ProfileQC(d)

samp = cruise.auxiliary['TEMP']['spike'].compressed()
samp = cruise.auxiliary['TEMP']['step'].compressed()
samp = cruise.auxiliary['common']['descentPrate'].compressed()
#samp = ped.auxiliary['TEMP']['gradient'].compressed()
#samp = ped.auxiliary['TEMP']['spike'].compressed()

samp=cruise.auxiliary['common']['descentPrate']

param = norm.fit(samp) # distribution fitting
param = rayleigh.fit(samp)
#param = exponweib.fit(samp)

# now, param[0] and param[1] are the mean and 
# the standard deviation of the fitted distribution
x = linspace(samp[ind].min(), samp[ind].max(), 100)
# fitted distribution
pdf_fitted = rayleigh.pdf(x,loc=param[0],scale=param[1])
# original distribution
pdf = norm.pdf(x)

#kstest(x, 'norm')

title('Normal distribution')
plot(x,pdf_fitted,'r-',x,pdf,'b-')
hist(samp, 100, normed=1,alpha=.3)
show()




import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

loc1, scale1, size1 = (-2, .1, 175)
x2 = np.random.normal(loc=loc1, scale=scale1, size=size1)
x_eval = np.linspace(x2.min() - 1, x2.max() + 1, 500)
pdf = stats.norm.pdf
bimodal_pdf = pdf(x_eval, loc=loc1, scale=scale1)
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111)
ax.plot(x2, np.zeros(x2.shape), 'b+', ms=12)
ax.plot(x_eval, bimodal_pdf, 'r--', label="Actual PDF")
ax.set_xlim([x_eval.min(), x_eval.max()])
ax.set_xlabel('x')
ax.set_ylabel('Density')
plt.show()


import pylab

pylab.plot(ped['TEMP'], -ped['pressure'])
pylab.plot(ped['TEMP'], -ped['pressure'], 'ro')
pylab.show()
