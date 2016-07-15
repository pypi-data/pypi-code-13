"""
Some basic functions for check points/shapes with shapefile data

Author: Cody Hanson
Date: 14 July 2016
"""

import geopandas as gpd

def is_point_in_shape(point_lat, point_lon, shape_object):
    """Check to see if a (latitude, longitude) point is within a shape"""
    return shape_object.contains(gpd.geoseries.Point(point_lat, point_lon))

def percent_intersect(shape_object_1, shape_object_2):
    """What percentage of shape 1 intersects with shape 2"""
    (gs1, gs2) = (gpd.GeoSeries(shape_object_1), gpd.GeoSeries(shape_object_2))
    (df1, df2) = (gpd.GeoDataFrame({'geometry' : gs1,
                                    'df1' : [1]}), gpd.GeoDataFrame({'geometry' : gs2, 'df2' : [1]}))
    intersection = gpd.overlay(df1, df2, how='intersection').geometry
    return intersection.area / shape_object_1.area
