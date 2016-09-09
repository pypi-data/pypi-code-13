### ERS cutout
if False:
    im = pyfits.open("/Users/brammer/3DHST/Spectra/Work/3DHST_Detection/GOODS-S_IR.seg.fits")
    slx, sly = slice(11039,15039), slice(14501,18151)
    wcs = pywcs.WCS(im[0].header)
    slice_wcs = wcs.slice((sly, slx))
    header = grizli.utils.to_header(slice_wcs)
    data = im[0].data[sly, slx]
    pyfits.writeto('../Catalog/ERS_GOODS-S_IR.seg.fits', data=data, header=header, clobber=True)
    ids = np.unique(data)
    cat = catIO.Table('/Users/brammer/3DHST/Spectra/Work/3DHST_Detection/GOODS-S_IR.cat')
    ix = cat['NUMBER'] == 0
    for i in range(len(cat['NUMBER'])):
        ix[i] = cat['NUMBER'][i] in ids
    
    for col in ['MAG_APER', 'MAGERR_APER', 'FLUX_APER', 'FLUXERR_APER']:
        cat.remove_column(col)
    
    cat[ix].write('../Catalog/ERS_GOODS-S_IR.cat', format='ascii.commented_header')
    
###### Grizli Demo
import glob
import time
import grizli

files = glob.glob('../RAW/*flt.fits')
info = grizli.utils.get_flt_info(files)
visits, filters = grizli.utils.parse_flt_files(info=info, uniquename=True)
direct = visits[0]
grism = visits[2] # ERS

# direct = {'files': ['ibhj34h6q_flt.fits', 'ibhj34hgq_flt.fits', 
#                     'ibhj34hsq_flt.fits', 'ibhj34hzq_flt.fits'],
#           'product': 'goodss-34-bhj-34-084.0-f140w'}
# 
# grism = {'files': ['ibhj34h8q_flt.fits', 'ibhj34hiq_flt.fits', 
#                    'ibhj34huq_flt.fits', 'ibhj34i1q_flt.fits'],
#          'product': 'goodss-34-bhj-34-084.0-g141'}

###############
### Background subtraction, astrometric alignment
from grizli.prep import process_direct_grism_visit

radec = '../Catalog/goodss_radec.dat'
t0 = time.time()
status = process_direct_grism_visit(direct=direct, grism=grism, 
                                    radec=radec,
                                    align_mag_limits=[14,23])
t1 = time.time()
print 'Image prepration, time: %.1f seconds' %(t1-t0)



### `GroupFLT` object for grism extraction, with grism exposures as input
### along with reference images and SExtractor catalog.
from grizli.multifit import GroupFLT, MultiBeam, get_redshift_fit_defaults

# grp = GroupFLT(grism_files=grism['files'], direct_files=[], 
#                ref_file='%s_drz_sci.fits' %(direct['product']),
#                seg_file='%s_seg.fits' %(direct['product']),
#                catalog='%s.cat' %(direct['product']), cpu_count=8)

all_grism_files = []
for i in range(len(visits)):
    if '-g1' in visits[i]['product']:
        all_grism_files.extend(visits[i]['files'])
        
grp = GroupFLT(grism_files=all_grism_files, direct_files=[], 
              ref_file='../Catalog/ERS_goodss_3dhst.v4.0.F160W_orig_sci.fits',
              seg_file='../Catalog/ERS_GOODS-S_IR.seg.fits',
              catalog='../Catalog/ERS_GOODS-S_IR.cat',
              cpu_count=8)

### Compute the flat continuum model
grp.compute_full_model(mag_limit=25)

### Refine the (polynomial) continuum model for brighter objects
t0 = time.time()
grp.refine_list(poly_order=2, mag_limits=[16, 24], verbose=True)
t1 = time.time()
print 'Refine model, time: %.1f seconds' %(t1-t0)

###############
### Extract "beam" spectra for a given object
t0 = time.time()
id = 117 # in corresponding catalog/segmentation image
id = 26087 # in master image
id = 26698 # 137
id = 41796 # ers
beams = grp.get_beams(id, size=80)
mb = MultiBeam(beams, fcontam=1, group_name='ers-grism')
t1 = time.time()

### Fit parameters
pzfit, pspec2, pline = get_redshift_fit_defaults()
pzfit ['zr'] = zr #[0.5, 2.4]
pzfit['dz'] = [0.005, 0.0005]
pline = {'kernel': 'square', 'pixfrac': 0.6, 'pixscale': 0.1, 'size': 20}
pspec2 = {'NY': 20, 'dlam': 40, 'spatial_scale': 1}

### Run the redshift fit and generate the emission line map
out = mb.run_full_diagnostics(pzfit=pzfit, pspec2=pspec2, pline=pline,
                              GroupFLT=grp, prior=None)

fit, fig, fig2, hdu2, hdu_line = out
t2 = time.time()
print '%.2f %.2f' %(t1-t0, t2-t1)

### Drizzled narrowband image
im = pyfits.open('/Users/brammer/3DHST/Ancillary/UDF/XDF/hlsp_xdf_hst_acswfc-60mas_hudf_f435w_v1_drz.fits')
ref_header = im[0].header

if True:
    wcs = pywcs.WCS(ref_header)
    sly, slx = slice(3264, 3731, 1), slice(2910, 3645, 1)
    sly, slx = slice(2745, 2985, 1), slice(2396, 2636, 1)
    wcs_slice = wcs.slice((sly, slx))
    ref_header = grizli.utils.to_header(wcs_slice)
    ref_header['NAXIS1'] = (slx.stop-slx.start)/slx.step
    ref_header['NAXIS2'] = (sly.stop-sly.start)/sly.step
    
# dl = 20
# zbest = 1.098024
if True:
    waves = [6564.61*(1+zbest)+dl]
    #waves = [5008.*(1+zbest)+dl]
#waves = np.arange(1.2e4,1.6e4,40)

for wave in waves:
    outsci, outwht = grp.drizzle_full_wavelength(wave=wave,
                                ref_header=ref_header, kernel='point',
                                pixfrac=0.5, verbose=True, offset=offset)
    ds9.view(outsci, header=ref_header)

    fig = plt.figure(figsize=np.array(outsci.shape)[::-1]/100.)
    ax = fig.add_subplot(111)
    ax.imshow(outsci, origin='lower', cmap='cubehelix_r', vmin=-0.01, vmax=0.05)
    ax.set_xticklabels([]); ax.set_yticklabels([])
    ax.text(0.03, 0.03, r'$\lambda=%.1f$' %(wave), color='k', ha='left', va='bottom', transform=ax.transAxes)

    fig.tight_layout(pad=0.01)
    fig.savefig('/tmp/udf_%06.1f.png' %(wave))
    print 'wave %.1f' %(wave)
    plt.close(fig)
    

# internal continuum
outconp, outwhtp = grp.drizzle_full_wavelength(wave=6564.61*(1+fit['zbest'])+200,
                            ref_header=ref_header, kernel='square',
                            pixfrac=0.8, verbose=True)

outconn, outwhtn = grp.drizzle_full_wavelength(wave=6564.61*(1+fit['zbest'])-200,
                            ref_header=ref_header, kernel='square',
                            pixfrac=0.8, verbose=True)

### Change line drizzle parameters
pline['kernel'] = 'square'
pline['pixscale'] = 0.06
pline['pixfrac'] = 0.8
hdu_full = mb.drizzle_fit_lines(fit, pline, 
                          force_line=['Ha','OIII','Hb','OII'], save_fits=True)

### Test WCS slice
# im = pyfits.open('goodss-34-bhj-34-084.0-f140w_drz_sci.fits')
# im = pyfits.open('/Users/brammer/3DHST/Ancillary/UDF/XDF/hlsp_xdf_hst_acswfc-60mas_hudf_f435w_v1_drz.fits')
# wcs = pywcs.WCS(im[0].header, relax=True)
# hdu_full = mb.drizzle_fit_lines(fit, pline, wcs=wcs,
#                           force_line=['Ha','OIII','Hb','OII'], save_fits=True)
# 
# ### Full....
# grp = GroupFLT(grism_files=glob.glob('*flt.fits'), direct_files=[], 
#                ref_file='goodss-mosaic-f160w_drz_sci.fits',
#                seg_file='goodss-mosaic_seg.fits',
#                catalog='goodss-mosaic_detection.cat', cpu_count=8)
