from collections import defaultdict
import json
import os
import time

__author__ = 'PyBeaner'

CACHE_PATH = os.path.join(os.path.expanduser('~'), '.cache/meipai')
SEARCH_RESULT_FILE = 'search_result.json'


# Get Cache
def check_cache_and_return_result(query, search_type, page):
    file_path = os.path.join(CACHE_PATH, SEARCH_RESULT_FILE)
    if os.path.exists(file_path):
        if time.time() - os.path.getmtime(file_path) > 15 * 60:
            # expired
            os.remove(file_path)
            return False, []
        try:
            data = json.loads(open(file_path).read())
            return True, data[search_type][query][str(page)]
        except KeyError as e:
            pass
    return False, []


# Cache the result
def cache_search_result(query, search_type, page, result):
    os.makedirs(CACHE_PATH, exist_ok=True)
    file_path = os.path.join(CACHE_PATH, SEARCH_RESULT_FILE)
    with open(file_path, 'w+') as file:
        try:
            data = json.loads(file.read())
        except Exception as e:
            data = defaultdict(dict)
        data.setdefault(search_type, {}).setdefault(query, {}).setdefault(page, result)
        file.write(json.dumps(data))


def get_last_page(query, search_type):
    file_path = os.path.join(CACHE_PATH, SEARCH_RESULT_FILE)
    try:
        data = json.loads(open(file_path).read())
        results = data[search_type][query]
        return int(max(results.keys()))
    except Exception as e:
        return 0
