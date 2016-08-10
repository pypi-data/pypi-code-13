from __future__ import print_function
import googlemaps
import requests
import webbrowser

API_KEY = 'AIzaSyA0TPKemHTbHfJV9dvE2TwwDEGZzSbERwM'

gmaps = googlemaps.Client(key=API_KEY)

def get_address_from_coords(coords):
    print("Getting address from coordinates ...")
    try:
        address = gmaps.reverse_geocode(coords)
        print("Done !")
        return address[0]['formatted_address']
    except:
        print("Oops ! Something went wrong, please try again shortly.")

def launch_map(address):
    print('Launching map ...')
    url = 'https://maps.googleapis.com/maps/api/staticmap?'
    params = {
        'center': address,
        'zoom': 17,
        'size': '1280x720',
        'maptype': 'roadmap',
        'markers': 'color:blue|' + address,
        'key': 'AIzaSyAsdkC6swEl9fjTHD3jjtLj9-JWHm-YqM0',
    }
    map_request = requests.get(url, params=params)
    webbrowser.open(map_request.url)

