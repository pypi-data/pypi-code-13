__version__ = '0.0.4'
import argparse
import webbrowser
import requests
from api_functions import *

def main():
    # Just a test comment to see if the version bump using tags actually works
    parser = argparse.ArgumentParser(description="Wrapper around the foursquare API. Use it to retrieve information about\
                                     specific venues or groups of venues.")
    parser.add_argument("endpoint", help="Name of the resource you want to access", choices=["categories", "trending",\
                                                                                             "explore", "search"])
    parser.add_argument("client_id", help="Your Foursquare Client ID")
    parser.add_argument("client_secret", help="Your Foursquare Client Secret")
    args = parser.parse_args()

    payload = {
        "v": 20160612,
        "m": "foursquare",
        "client_id": args.client_id,
        "client_secret": args.client_secret
    }

    if args.endpoint == "categories":
        get_categories(payload)
    elif args.endpoint == "search":
        search_venues(payload)
    elif args.endpoint == "trending":
        get_trending_venues(payload)
    elif args.endpoint == "explore":
        explore_venues(payload)
