#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

from datetime import datetime
import random

import numpy as np
from numpy import ma

from oceansdb.etopo import ETOPO

def test_import():
    # A shortcut
    from oceansdb import ETOPO
    db = ETOPO()


def test_available_vars():
    db = ETOPO()
    
    for v in ['elevation']:
        assert v in db.keys()


# ==== Request points coincidents to the ETOPO gridpoints
def test_coincident_gridpoint():
    db = ETOPO()

    h = db.extract(lat=17.5, lon=0)
    assert np.allclose(h['elevation'], [305.])


    h = db.extract(lat=[17.5, 18.5], lon=0)
    assert np.allclose(h['elevation'], [305., 335.])

    h = db.extract(lat=17.5, lon=[359.92, 0])
    assert np.allclose(h['elevation'], [305., 305.])

    h = db.extract(lat=[17.5, 18.5], lon=[-0.08, 0])
    assert np.allclose(h['elevation'], [[305., 305.], [335., 335.]])


def test_lon_cyclic():
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


#def test_badlocation():
def test_extract_lat_overlimit():
    """ Thest a request over the limits of the database """
    db = ETOPO()

    lon0 = random.uniform(-180, 360)
    coords = [[91, lon0], [-91, lon0], [90.01, lon0]]
    for lat, lon in coords:
        try:
            h = db.extract(lat=lat, lon=lon)
        except ValueError:
            print("Correct type of error.")
            raise
        except:
            assert False, "Coordinate overlimit should return ValueError"

# ======


def notest_get_point():
    db = ETOPO()

    t = db['TEMP'].extract(var='t_mn', doy=90,
            depth=0, lat=17.5, lon=-37.5)
            #depth=0, lat=10, lon=330)
    assert np.allclose(t['mn'], [24.60449791])


def notest_get_profile():
    db = ETOPO()


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
    db = ETOPO()
    db['TEMP'].get_track(doy=[datetime.now()], depth=0, lat=[10], lon=[330])
    db['TEMP'].get_track(doy=2*[datetime.now()], depth=0, lat=[10, 12], lon=[330, -35])
