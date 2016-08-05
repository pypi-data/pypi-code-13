from helpers import *
from api_helpers import *

def get_categories(payload):
    print("Fetching categories ...")
    make_request('categories', payload)

def search_venues(payload):
    payload['query'] = get_search_query()
    payload['near'] = get_location()
    radius = get_radius()
    limit = get_limit()
    category_id = get_category_id()

    if radius: payload['radius'] = radius
    if limit: payload['limit'] = limit
    if category_id: payload['category_id'] = category_id

    print("Fetching %s venues in %s ..." % (payload['query'], payload['near']))
    make_request('search', payload)

def get_trending_venues(payload):
    payload['near'] = get_location()
    radius = get_radius()
    limit  = get_limit()

    if radius: payload['radius'] = radius
    if limit: payload['limit'] = limit

    print("Fetching trending venues in %s" % (payload['near']))
    make_request('trending', payload)

def explore_venues(payload):
    payload['near'] = get_location()
    query = get_search_query(required=False)
    section = get_section()
    price = get_price_range()
    limit = get_limit()

    if query: payload['query'] = query
    if section: payload['section'] = section
    if price: payload['price'] = price
    if limit: payload['limit'] = limit

    print("Exploring venues in %s" % (payload['near']))

    make_request('explore', payload)

