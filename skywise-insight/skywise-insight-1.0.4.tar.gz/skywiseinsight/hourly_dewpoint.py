# -*- coding: utf-8 -*-
"""
    skywiseinsight.hourly_dewpoint
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Implementation of the Hourly Dewpoint resource.

    :copyright: (c) 2016 by WDT Inc.
    :license: MIT, see LICENSE for more details.
"""
from voluptuous import Any

from ._hourly_resource import (HourlyResourceLocation,
                               HourlyTimeSeriesResourceAsset,
                               HourlyResourceContourByValidTime)


class HourlyDewpoint(object):

    @classmethod
    def location(cls, lat, lon, start=None, end=None, unit=None, **kwargs):
        """Retrieves Hourly Dewpoint time series data for a specified point.

        :ivar float lat: Latitude
        :ivar float lon: Longitude
        :ivar datetime start: Start of your query.
        :ivar datetime end: End of your query.
        :ivar string unit: 'fahrenheit' or 'celsius'
        """
        return _HourlyDPByLocation.find(latitude=lat, longitude=lon,
                                        start=start, end=end, unit=unit, **kwargs)

    @classmethod
    def asset(cls, asset_uuid, start=None, end=None, unit=None, **kwargs):
        """Retrieves Hourly Dewpoint areal statistics and time series data for the specified asset.

        :ivar string asset_uuid: Asset UUID
        :ivar datetime start: Start of your query.
        :ivar datetime end: End of your query.
        :ivar string unit: 'fahrenheit' or 'celsius'
        """
        return _HourlyDPByAsset.find(asset_uuid=asset_uuid, start=start, end=end,
                                     unit=unit, **kwargs)

    @classmethod
    def contours(cls, asset_uuid, valid_time=None, unit=None, **kwargs):
        """Retrieves Hourly Dewpoint areal statistics and time series data for the specified asset.

        :ivar string asset_uuid: Asset UUID
        :ivar datetime valid_time: The datetime you're requesting contours for.
        :ivar string unit: 'fahrenheit' or 'celsius'
        """
        return _HourlyDPContours.find(asset_uuid=asset_uuid, validTime=valid_time,
                                      unit=unit, **kwargs)


class _HourlyDPByLocation(HourlyResourceLocation):

    _path = '/hourly-dewpoint/{latitude}/{longitude}'

    _args = HourlyResourceLocation._args.extend({
        'unit': Any('Celsius', 'Fahrenheit', 'celsius', 'fahrenheit')
    })


class _HourlyDPByAsset(HourlyTimeSeriesResourceAsset):

    _path = '/hourly-dewpoint/{asset_uuid}'

    _args = HourlyTimeSeriesResourceAsset._args.extend({
        'unit': Any('Celsius', 'Fahrenheit', 'celsius', 'fahrenheit')
    })


class _HourlyDPContours(HourlyResourceContourByValidTime):

    _path = '/hourly-dewpoint/{asset_uuid}/contours'

    _args = HourlyResourceContourByValidTime._args.extend({
        'unit': Any('Celsius', 'Fahrenheit', 'celsius', 'fahrenheit')
    })
