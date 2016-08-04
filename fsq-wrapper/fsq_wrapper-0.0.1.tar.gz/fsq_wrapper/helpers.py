from input_helpers import *

def get_search_query(required=True):
    query_message = "Please provide a search query "

    if required == False:
        return get_string(query_message + "(Leave blank to skip):")
    else:
        return get_required_string(query_message + "(Required):")

def get_location():
    return get_required_string("Please provide a Location: ")

def get_limit():
    return check_in_range("How many results to you want to return ? (Up to 50 - Default: 10) Leave blank to skip:", \
                          1, 50, 10)
def get_radius():
    return check_in_range("Please provide a search radius (in meters - Up to 2000 - Default: 100) \
 Leave blank to skip:", 1, 2000, 100)

def get_section():
    section_list = ['food', 'drinks', 'coffee', 'shops', 'arts', 'outdoors', 'sights', 'trending', 'specials']
    return check_in_list("Please select a section (Food, Drinks, Coffee, Shops, Arts, Outdoors, Sights, Trending,\
 Specials) Leave blank to skip", section_list)

def get_price_range():
    return check_in_range("Do you want to filter by price range ? (Choose between 1 and 4 - 1 being the least\
 expensive) - Default is 2 - Leave blank to skip", 1, 4, 2)

def get_category_id():
    return get_string("Please provide a category id (Must be separated by commas, Leave blank to skip)")

