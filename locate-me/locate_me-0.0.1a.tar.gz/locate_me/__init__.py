import argparse
from helpers import *
from maps import *

parser = argparse.ArgumentParser(description="CLI Tool to extract geolocation data from images")
parser.add_argument("image", help="The path to the image you want to parse")
args = parser.parse_args()

def main(args):

    if args.image:
        img = open_image(args.image)
        data = get_exif_data(img)
        gps_info = get_gps_info(data)
        latlng = convert_to_lat_lng(gps_info)
        address = get_address_from_coords(latlng)
        launch_map(address)

main(args)
