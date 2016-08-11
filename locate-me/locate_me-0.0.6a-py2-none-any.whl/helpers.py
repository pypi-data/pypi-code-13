from __future__ import print_function
from PIL import Image
from PIL.ExifTags import TAGS
import json

def open_image(path):
    img = Image.open(path)
    return img

def get_exif_data(img_obj):
    tags = img_obj._getexif()

    try:
        metadata = {}
        if tags:
            print("Found meta data ! Scanning ...")
            for tag, value in tags.items():
                tagname = TAGS.get(tag)
                metadata[tagname] = value
            return metadata
    except:
        print("Sorry, no Exif data could be retrived from this image")


def get_gps_info(exifData):
    print("Scanning for coordinates ...")
    try:
        gpsInfo = exifData['GPSInfo']
        lat = [gpsInfo[2][0][0], gpsInfo[2][1][0], gpsInfo[2][2][0]]
        lon = [gpsInfo[4][0][0], gpsInfo[4][1][0], gpsInfo[4][2][0]]

        if lat and lon:
            print("Found LatLng values")
            return lat, lon
        else:
            print("Sorry no usable GPS info could be retrived")
    except:
        print("Sorry bruv, no GPS info is available for this image")

def convert_to_lat_lng(coords):
    try:
        lat_values = coords[0]
        lon_values = coords[1]

        dlat = lat_values[0] + (lat_values[1] / 60.0) + (lat_values[1] / 3600.0)
        dlon = lon_values[0] + (lon_values[1] / 60.0) + (lon_values[1] / 3600.0)

        return dlat, dlon
    except:
        print("No coordinates to convert, sorry bruv")
