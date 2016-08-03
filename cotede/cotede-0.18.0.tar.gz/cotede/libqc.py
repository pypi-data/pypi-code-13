"""

    ATENTION, I should change this. The basic class should handle one profile, even
    that making the procedure less efficient for the whole DB update. On this way,
    the input should be a dictionary {depth, lat, lon, datetime, temp, salt, temp1...}
    Than I have a function like, evaluate('temperature') and returns a dictionary
    with the flags for each test. On the top of this I can make another class
    to use it to update the database.

    UPDATE pirata_raw.data SET temperature_qc=-1 WHERE id IN (SELECT id from pirata_raw.data_flags WHERE (human_evalt=False OR climatology_t=False OR global_ranget=False OR not_spiket=False OR not_gradientt=False OR not_digit=False OR climatology_t=False));

    UPDATE pirata_raw.data SET temperature_qc=1 WHERE id IN (SELECT id from pirata_raw.data_flags WHERE human_evalt=True OR ((climatology_t=TRUE OR global_ranget=TRUE OR not_spiket=TRUE OR not_gradientt=TRUE OR not_digit=TRUE OR climatology_t=TRUE) AND (climatology_t!=False AND global_ranget!=False AND not_spiket!=False AND not_gradientt!=False AND not_digit!=False AND climatology_t!=False))); 

    UPDATE ctd.data SET temperature_qc=-1 WHERE id IN (SELECT id from ctd.data_flag WHERE (human_evalt=False OR climatology_t=False OR global_ranget=False OR not_spiket=False OR not_gradientt=False OR not_digit=False OR climatology_t=False));


# Looks like bellow here is the right way to do it.


UPDATE ctd.data SET temperature_qc = 1 WHERE id IN (SELECT id FROM ctd.data_flag where measure ='t' AND (global_range=True AND (human_eval=True OR (not_spike=True OR not_gradient=True OR not_digitrollover=True OR climatology=True))));
UPDATE ctd.data SET temperature_qc=-1 WHERE id IN (SELECT id FROM ctd.data_flag WHERE measure='t' AND (human_eval=False OR climatology=False OR global_range=False OR not_spike=False OR not_gradient=False OR not_digitrollover=False));


UPDATE ctd.data SET salinity_qc = 1 WHERE id IN (SELECT id FROM ctd.data_flag where measure ='s' AND (global_range=True AND (human_eval=True OR (not_spike=True OR not_gradient=True OR not_digitrollover=True OR climatology=True))));
UPDATE ctd.data SET salinity_qc=-1 WHERE id IN (SELECT id FROM ctd.data_flag WHERE measure='s' AND (human_eval=False OR climatology=False OR global_range=False OR not_spike=False OR not_gradient=False OR not_digitrollover=False));

"""

import numpy
import numpy as np
from numpy import ma

from pydap.client import open_url
import pydap.lib
pydap.lib.CACHE = '.cache'
from scipy.interpolate import RectBivariateSpline

import libsql
import misc
# ============================================================================

def atsea_test(lat,lon):
    """
    """
    flag = ma.ones(lat.shape, dtype=numpy.bool)
    flag[misc.get_depth(lat, lon)>0] = False
    return flag

def gradient(x):
    y = ma.masked_all(x.shape)
    y[1:-1] = numpy.abs(x[1:-1] - (x[:-2] + x[2:])/2.0)
    # ATENTION, temporary solution
    #y[0]=0; y[-1]=0
    return y

def gradient_test(x, threshold, loop=False):
    """
    """
    flag = ma.masked_all(x.shape, dtype=numpy.bool)
    g = gradient(x)
    flag[numpy.nonzero(g>threshold)] = False
    flag[numpy.nonzero(g<=threshold)] = True
    return flag

def spike(x):
    y = ma.masked_all(x.shape)
    y[1:-1] = numpy.abs(x[1:-1] - (x[:-2] + x[2:])/2.0) - numpy.abs((x[2:] - x[:-2])/2.0)    # ATENTION, temporary solution
    #y[0]=0; y[-1]=0
    return y

def spike_test(x, threshold, loop=False):
    """
    """
    flag = ma.masked_all(x.shape, dtype=numpy.bool)
    flag[numpy.nonzero(spike(x)>threshold)] = False
    flag[numpy.nonzero(spike(x)<=threshold)] = True
    return flag

class QC(object):
    """ Apply the QC tests
    """
    def __init__(self, cfg):
        """
        """
        self.cfg = cfg

        self.set_conn()
        cur = self.conn.cursor()
	cur.execute("SELECT id from %s;" % ('ctd.station'))
	#pids = cur.fetchall()
	pids = [p[0] for p in cur.fetchall()]
        pids.sort()
	for p in pids:
	    print "Working on profile %s" % p
            perfil = libsql.profile_dict(connection=self.conn, pid=p, 
                table_station=cfg['table_station'], table_data=cfg['table_data'])
            pqc = ProfileQC(perfil, cfg)
	    for var, measure in [['salinity', 's'], ['temperature', 't']]:
                pqc.evaluate(var)
                #measure='t'
                ids = pqc.input['id']
                # Damn stupid retarded way to do it.
                for n, i in enumerate(ids):
                    cur.execute("SELECT id from %s WHERE id=%s AND measure='%s';" % ('ctd.data_flag', i, measure))
                    if cur.rowcount == 0:
                        cur.execute("INSERT INTO %s (id, measure) VALUES (%s,'%s');" % ('ctd.data_flag', i, measure))
                self.conn.commit()
                for test in ('global_range', 'not_spike', 'not_gradient', 'not_digitrollover'):
                    flags = pqc.flags[test]
                    for i in ma.nonzero(ma.getmaskarray(pqc.flags[test])==False)[0]:
                        query = "UPDATE %s SET %s=%s WHERE measure='%s' AND id=%s;" % \
                            ('ctd.data_flag', test, flags[i], measure, ids[i])
                        cur.execute(query)
                    self.conn.commit()

        
        
        #self.qc_atsea()
        #self.qc_global_range()
	#self.gradient_test()
	#self.spike_test()
    
    def set_conn(self):
        """
        """
        self.conn = libsql.set_connection(self.cfg['psql'])

    def at_sea(self, pqc):
	# ---- At Sea ----
        query = "UPDATE %s SET %s=%s WHERE id=%s;" % \
            ('ctd.station_flags', 'at_sea', pqc.flags['at_sea'][0], pqc.input['pid'][0])
        cur = self.conn.cursor()
        cur.execute(query)
        self.conn.commit()
        #self.logger.debug("Profile %s at_sea %s" % (pqc.input['pid'], pqc.flags['at_sea'])) 

class ProfileQC(object):
    """Apply the QC tests into a profile
    """
    def __init__(self, input, cfg):
        """

            input -> datetime, latitude, longitude, data
            cfg -> min_range, max_range, max_gradient
        """
        self.input = input
        self.cfg = cfg
        self.flags = {}
        self.data = {}
        try:
            self.at_sea()
        except:
            print "Couldn't run at_sea test"

    def evaluate(self, var):
        self.var = var
        self.global_range(var)
        self.digit(var)
        self.gradient(var)
        self.spike(var)
        try:
            self.woa_anom(var)
        except:
            print "Couldn't run climatology test"

    def global_range(self, var):
        """
        """
        cfg = self.cfg[var]['global_range']
        flag = ma.masked_all(self.input[var].shape, dtype=numpy.bool)
        flag[ (self.input[var] >= cfg['min']) & 
                (self.input[var] <= cfg['max'])] = True
        flag[ (self.input[var] < cfg['min']) | 
                (self.input[var] > cfg['max'])] = False
        self.flags['global_range'] = flag

    def at_sea(self):
        """
        """
        #flag = ma.masked_all(self.input[var].shape, dtype=numpy.bool)
        depth = misc.get_depth(self.input['latitude'], self.input['longitude'])
        #flag[depth<0] = True
        #flag[depth>0] = False
        #self.flags['at_sea'] = flag
        self.flags['at_sea'] = depth<0

    def digit(self, var):
        """
        """
        cfg = self.cfg[var]['digit']
        flag = ma.masked_all(self.input[var].shape, dtype=np.bool)
        step = ma.masked_all(self.input[var].shape, dtype=np.float)
        step[1:] = ma.absolute(ma.diff(self.input[var]))
        flag[ma.absolute(step)>cfg] = False
        flag[ma.absolute(step)<=cfg] = True
        self.flags['not_digitrollover'] = flag
        self.data['step'] = step

    def gradient(self, var):
        """
        """
        cfg = self.cfg[var]['gradient']
        flag = ma.masked_all(self.input[var].shape, dtype=numpy.bool)
        g = gradient(self.input[var])
        flag[g>cfg['max']] = False
        flag[g<=cfg['max']] = True
        self.flags['not_gradient'] = flag
        self.data['gradient'] = g

    def spike(self, var):
        """
        """
        cfg = self.cfg[var]['spike']
        flag = ma.masked_all(self.input[var].shape, dtype=numpy.bool)
        s = spike(self.input[var])
        flag[s>cfg['max']] = False
        flag[s<=cfg['max']] = True
        self.flags['not_spike'] = flag
        self.data['spike'] = s

    def woa_anom(self, var):
        """

            ATENTION, I think WOA runs on depth, not pressure.
        """
        self.data['woa'] = misc.woa_profile_from_dap(var, self.input['doy'], self.input['latitude'], self.input['longitude'], self.input['pressure'])
        self.data['woa_anom'] = self.input[var] - self.data['woa']





# Probably do not use this, but straight inside the psql.
def globalrange_test(data, tresholdmin, tresholdmax):
    """
    Global test function, according to NOAA's Q.C Manual.
    
    """
    #flag = ma.ones(data.shape, dtype=numpy.bool)
    flag = ~ma.getmaskarray(data)
    flag[(data<tresholdmin) | (data>tresholdmax)] = False
    return flag

def digitrollover_test(data, theshold):
    """

        This looks like a pertinent test, but there are things to be
          improved here. Maybe I'm overthinking and agregating issues related
          to gradient and spike here?!

        Need to think about this test:
        - How to deal with the case where the first sample is a bad rollover
            case and the second is good?
        - Is it pertinent to apply with a loop? Should I check the jump in
            respect to the last valid data?
        - How to handle the case where several records where null? The
            following valid data could have a considerable jump
    """
    return
    # these are from an old version. Probably not the best way to do it.
    indices = np.arange(len(data)).compress(~np.ma.getmaskarray(data))  #compress in where mask None==True (then use "~" to get the Falses, that being where data is not None, therefore exists
    treshold = treshold.compress(~np.ma.getmaskarray(data))
    data = data.compressed()
    apply_test = True
    while apply_test:
        test = np.ones(data.shape, bool)
        test[:-1]= abs(data[:-1] - data[1:]) < (treshold[:-1])# True for valid data
        data = data.compress(test)
        indices = indices.compress(test)
        treshold = treshold.compress(test)
        apply_test = np.any(~test) and loop  #while there is a "False" flag, the loop continues, if it was established loop=true in the function
    # return indices where data is good  
    return indices

