import numpy as np
import connectivipy as cp
import time

wrdata = np.fromfile('wronski_82t.dat',dtype=np.float32)

nrchannels = 65
fs = 125
intr_channs = [12,10,5,60,6,14,57,22,16,51,49,28,34,42,30,44]
dllen = 407
nroftrials = 30
alldata = np.zeros((nrchannels, dllen, nroftrials))

for i in range(nrchannels):
    for k in range(nroftrials-1):
        alldata[i,:,k] = wrdata[i::nrchannels][k*dllen:(k+1)*dllen]

chdata = alldata[intr_channs, :, :]

dd = cp.Data(chdata, fs)
estm = dd.short_time_conn('dtf', order=5, nfft=40, no=5)
t0 = time.time()
dd.plot_short_time_conn("DTF", show=True)
print(time.time()-t0)
