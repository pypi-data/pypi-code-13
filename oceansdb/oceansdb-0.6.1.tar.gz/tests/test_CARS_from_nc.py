#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

from datetime import datetime

import numpy as np
from numpy import ma

from oceansdb.cars import CARS

def test_import():
    # A shortcut
    from oceansdb import CARS
    db = CARS()


def test_available_vars():
    db = CARS()
    
    for v in ['TEMP', 'PSAL']:
        assert v in db.keys()


# ==== Request points coincidents to the CARS gridpoints
def test_coincident_gridpoint():
    db = CARS()

    t = db['TEMP'].extract(var='mn', doy=100,
            depth=0, lat=17.5, lon=322.5)
    assert np.allclose(t['mn'], [23.78240879])

    t = db['TEMP'].extract(var='mn', doy=[100, 150],
            depth=0, lat=17.5, lon=322.5)
    assert np.allclose(t['mn'], [23.78240879, 24.57544294])

    t = db['TEMP'].extract(var='mn', doy=100,
            depth=[0, 10], lat=17.5, lon=322.5)
    assert np.allclose(t['mn'], [23.78240879, 23.97279877])

    t = db['TEMP'].extract(var='mn', doy=100,
            depth=0, lat=[17.5, 12.5], lon=322.5)
    assert np.allclose(t['mn'], [24.61333538, 23.78240879])

    t = db['TEMP'].extract(var='mn', doy=100,
            depth=0, lat=17.5, lon=[322.5, 327.5])
    assert np.allclose(t['mn'], [23.78240879, 24.03691995])

    t = db['TEMP'].extract(var='mn', doy=100,
            depth=[0, 10], lat=[17.5, 12.5], lon=322.5)
    assert np.allclose(t['mn'],
            [[24.61333538, 23.78240879], [24.7047015, 23.97279877]])


def notest_lon_cyclic():
    db = WOA()

    t1 = db['TEMP'].extract(var='t_mn', doy=136.875,
            depth=0, lat=17.5, lon=182.5)
    t2 = db['TEMP'].extract(var='t_mn', doy=136.875,
            depth=0, lat=17.5, lon=-177.5)
    assert np.allclose(t1['t_mn'], t2['t_mn'])

    t1 = db['TEMP'].extract(var='t_mn', doy=136.875,
            depth=0, lat=17.5, lon=[-37.5, -32.5])
    t2 = db['TEMP'].extract(var='t_mn', doy=136.875,
            depth=0, lat=17.5, lon=[322.5, 327.5])
    assert np.allclose(t1['t_mn'], t2['t_mn'])

def notest_no_data_available():
    """ This is a position without valid data """

    db = WOA()
    out = db['TEMP'].extract(doy=155, lat=48.1953, lon=-69.5855,
            depth=[2.0, 5.0, 6.0, 21.0, 44.0, 79.0, 5000])
    assert sorted(out.keys()) == [u't_dd', u't_mn', u't_sd', u't_se']
    for v in out:
        ma.getmaskarray(out[v]).all()

def notest_extract_overlimit():
    """ Thest a request over the limits of the database """
    db = WOA()

    t = db['TEMP'].extract(var='t_mn', doy=136.875,
            depth=5502, lat=17.5, lon=-37.5)
    assert ma.is_masked(t['t_mn'])

    t = db['TEMP'].extract(var='t_mn', doy=136.875,
            depth=[10, 5502], lat=17.5, lon=-37.5)
    assert np.all(t['t_mn'].mask == [False, True])
    assert ma.allclose(t['t_mn'],
            ma.masked_array([24.62145996, 0], mask=[False, True]))

# ======


def notest_get_point():
    db = WOA()

    t = db['TEMP'].extract(var='t_mn', doy=90,
            depth=0, lat=17.5, lon=-37.5)
            #depth=0, lat=10, lon=330)
    assert np.allclose(t['mn'], [24.60449791])


def notest_get_profile():
    db = WOA()


    t = db['TEMP'].extract(var='mn', doy=10,
            depth=[0,10], lat=10, lon=330)
    assert np.allclose(t['mn'], [ 28.09378815,  28.09343529])

    t = db['TEMP'].extract(doy=10,
            depth=[0,10], lat=10, lon=330)
    assert np.allclose(t['t_se'], [ 0.01893404,  0.0176903 ])
    assert np.allclose(t['t_sd'], [ 0.5348658,  0.4927946])
    assert np.allclose(t['t_mn'], [ 28.09378815,  28.09343529])
    assert np.allclose(t['t_dd'], [ 798, 776])


def notest_get_track():
    db = WOA()
    db['TEMP'].get_track(doy=[datetime.now()], depth=0, lat=[10], lon=[330])
    db['TEMP'].get_track(doy=2*[datetime.now()], depth=0, lat=[10, 12], lon=[330, -35])


def notest_dev():
    db = WOA()
    t = db['TEMP'].extract(doy=228.125, lat=12.5, lon=-37.5)
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

from datetime import datetime

import numpy as np
from numpy import ma

from oceansdb.etopo import ETOPO

def notest_import():
    # A shortcut
    from oceansdb import ETOPO
    db = ETOPO()


def notest_available_vars():
    db = ETOPO()
    
    for v in ['elevation']:
        assert v in db.keys()


# ==== Request points coincidents to the ETOPO gridpoints
def notest_coincident_gridpoint():
    db = ETOPO()

    h = db.extract(lat=17.5, lon=0)
    assert np.allclose(h['elevation'], [305.])


    h = db.extract(lat=[17.5, 18.5], lon=0)
    assert np.allclose(h['elevation'], [305., 335.])

    h = db.extract(lat=17.5, lon=[359.92, 0])
    assert np.allclose(h['elevation'], [305., 305.])

    h = db.extract(lat=[17.5, 18.5], lon=[-0.08, 0])
    assert np.allclose(h['elevation'], [[305., 305.], [335., 335.]])


def notest_lon_cyclic():
    db = ETOPO()

    h1 = db.extract(lat=17.5, lon=182.5)
    h2 = db.extract(lat=17.5, lon=-177.5)
    assert np.allclose(h1['elevation'], h2['elevation'])

    h1 = db.extract(lat=17.5, lon=[-37.5, -32.5])
    h2 = db.extract(lat=17.5, lon=[322.5, 327.5])
    assert np.allclose(h1['elevation'], h2['elevation'])

    lons = 360 * np.random.random(10)
    for lon1 in lons:
        h1 = db.extract(lat=17.5, lon=lon1)
        lon2 = lon1 - 360
        h2 = db.extract(lat=17.5, lon=lon2)
        assert np.allclose(h1['elevation'], h2['elevation']), \
                "Different elevation between: %s and %s" % (lon1, lon2)
