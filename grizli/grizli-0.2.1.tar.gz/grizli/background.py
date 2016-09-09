"""
Fit multi-component background
"""

def go():
    
    import os
    import glob
    import astropy.io.fits as pyfits
    
    # import mywfc3.flt.multifit
    # reload(mywfc3.grism); reload(mywfc3.flt.model); reload(mywfc3.flt.test_parallel); reload(mywfc3.flt.multifit)
    
    import grizlidev as grizli
    import grizlidev.multifit
    reload(grizli.model); reload(grizli.multifit); reload(grizli)
    
    #import threedhst.dq
    import pyds9
    ds9 = pyds9.DS9()
    
    grism = 'G141'
    
    all_files = glob.glob('*flt.fits')
    files=[]
    for file in all_files:
        im = pyfits.open(file)
        if im[0].header['FILTER'].startswith(grism):
            files.append(file)
    
    files.sort()
    
    files=files[20:24]
    
    group = grizli.multifit.GroupFLT(files, refimage='F160W_mosaic.fits', segimage='F160W_seg_blot.fits', master_cat='/Users/brammer/3DHST/Spectra/Work/3DHST_Detection/GOODS-N_IR.cat', pad=150)
    
    group.mp_compute_models(group.fit_data, initialize=True, verbose=1, parallel=True)
    group.refine_model(maglim=23, ds9=ds9)
    
    flat = pyfits.open('/Users/brammer/Research//HST/IREF//uc721143i_pfl.fits')
    gflat = pyfits.open('/Users/brammer/Research//HST/IREF//u4m1335mi_pfl.fits')
    flat[1].data /= gflat[1].data
    
    ### Test with original FLT data
    for i in range(group.N):
        im = pyfits.open(glob.glob('../RAW/%s*' %(group.FLTs[i].flt_file))[0])
        print im.filename()
        flt = group.FLTs[i]
        p = flt.pad
        flt.im_data['SCI'][p:-p,p:-p] = im[1].data/flat[1].data[5:-5,5:-5]
        
    ### Read in original FLT SCI
    self = group
    
def fit_multi_background(self, bg_fixed = ['zodi_G141_clean.fits'], bg_vary=['excess_G141_clean.fits']):
    
    bg_fixed = ['zodi_G141_clean.fits']
    bg_vary = ['zodi_G141_clean.fits', 'excess_G141_clean.fits', 'G141_scattered_light.fits'][1:-1]
    
    data_fixed = []
    for file in bg_fixed:
        im = pyfits.open('%s/CONF/%s' %(os.getenv('GRIZLI'), file))[0].data.flatten()
        data_fixed.append(im)
    
    #data_fixed.append(1+1.e-8*np.random.normal(size=1014**2))
    
    data_vary = []
    for file in bg_vary:
        im = pyfits.open('%s/CONF/%s' %(os.getenv('GRIZLI'), file))[0].data.flatten()
        data_vary.append(im)
    
    yp, xp = np.indices((1014,1014))
    
    # data_vary.append(1+1.e-14*np.random.normal(size=1014**2))    
    # data_vary.append(((xp-507)/507.).flatten())
    # data_vary.append(((yp-507)/507.).flatten())
              
    flt = self.FLTs[0]
    Npix = (flt.grism.sh[0]-2*flt.pad)**2
    
    Nfix = len(data_fixed)
    Nvary = len(data_vary)
    
    Nimg = self.N*Nvary + Nfix
    A = np.zeros((Npix*self.N, Nimg))
    
    data = np.zeros(Npix*self.N)
    mask = data > -1
    full_coeffs = np.zeros(Nimg)
    
    for i in range(self.N):
        flt = self.FLTs[i]
        p = flt.pad
        
        ## Data
        clean = flt.grism['SCI'] - flt.model
        data[i*Npix:(i+1)*Npix] = clean[p:-p,p:-p].flatten()
        mask[i*Npix:(i+1)*Npix] &= flt.grism['DQ'][p:-p,p:-p].flatten() == 0
        mask[i*Npix:(i+1)*Npix] &= flt.model[p:-p,p:-p].flatten() < 0.1
        
        #mask[i*Npix:(i+1)*Npix] &= xp.flatten() > 200
         
        for j in range(Nfix):
            for k in range(self.N):
                A[k*Npix:(k+1)*Npix,j] = data_fixed[j]
            
            mask[i*Npix:(i+1)*Npix] &= (data_fixed[j] > 0) & np.isfinite(data_fixed[j])
            
        for j in range(Nvary):
            k = Nfix+j+Nvary*i
            print 'i, k: %d %d' %(i, k)
            A[i*Npix:(i+1)*Npix,k] = data_vary[j]
            mask[i*Npix:(i+1)*Npix] &= np.isfinite(data_vary[j]) # & (data_vary[j] > 0) 
            
    
    # import sklearn.linear_model
    # clf = sklearn.linear_model.LinearRegression()
    # 
    # status = clf.fit(A[mask,:], data[mask])
    # coeffs = clf.coef_
    
    out = np.linalg.lstsq(A[mask,:], data[mask])
    coeffs = out[0]
    #m = np.dot(A, out[0])
    
    sky = np.dot(A, coeffs).reshape(self.N, Npix)
    full_coeffs += coeffs
    for i in range(self.N):
        data[i*Npix:(i+1)*Npix] -= sky[i,:]
    print coeffs
    
    sky = np.dot(A, full_coeffs).reshape(self.N, Npix)
    for i in range(self.N):
        sky_i = np.zeros_like(self.FLTs[i].grism['SCI'])
        sky_i[p:-p,p:-p] = sky[i,:].reshape((1014,1014))
        self.FLTs[i].grism.data['SCI'] -= sky_i*(self.FLTs[i].grism['SCI'] != 0)
        
    ### Test column avg
    i = 3
    f = (self.FLTs[i].grism['SCI'] - self.FLTs[i].model)[p:-p,p:-p]
    #clean = f - sky[i,:].reshape((1014,1014))
    clean = f
    m = mask[i*Npix:(i+1)*Npix].reshape((1014,1014))
    m &= (self.FLTs[i].model < 0.2*self.FLTs[i].grism['ERR'])[p:-p,p:-p]
    
    import numpy.ma
    ma = np.ma.masked_array(clean, mask=(~m))
    med = np.ma.median(ma, axis=0)
    pi = plt.plot(med, alpha=0.2)
    
    from sklearn.gaussian_process import GaussianProcess
    bg_sky = 1
    yrms = np.ma.std(ma, axis=0)/np.sqrt(np.sum(m, axis=0))
    xmsk = np.arange(1014)
    yres = med
    yok = ~yrms.mask
    
    gp = GaussianProcess(regr='constant', corr='squared_exponential', theta0=8,
                         thetaL=7, thetaU=12,
                         nugget=(yrms/bg_sky)[yok][::1]**2,
                         random_start=10, verbose=True, normalize=True) #, optimizer='Welch')
    #
    gp.fit(np.atleast_2d(xmsk[yok][::1]).T, yres[yok][::1]+bg_sky)
    y_pred, MSE = gp.predict(np.atleast_2d(xmsk).T, eval_MSE=True)
    gp_sigma = np.sqrt(MSE)
    gp_res = np.dot(y_pred[:,None]-1, np.ones((1014,1)).T).T
        
    plt.plot(y_pred-1, color=pi[0].get_color())
    plt.fill_between(xmsk, y_pred-1-gp_sigma, y_pred-1+gp_sigma, color=pi[0].get_color(), alpha=0.3)
