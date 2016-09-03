from __future__ import print_function
import sys
import requests
import json

API_URL = 'https://api.whatismymovie.com/1.0/'

'''
    eprint() is like print() but to stderr
'''
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

class Movie:
    '''
        Movie object
          movie.imdb_id       # integer for IMDB id
          movie.imdb_id_long  # full IMDB id (string)
          movie.title         # movie's title
          movie.year          # movie's pub. year
    '''
    def __init__(self, json_object):
        self.imdb_id = json_object['imdb_id']
        self.imdb_id_long = json_object['imdb_id_long']
        self.title = json_object['title']
        self.year = json_object['year']

class WhatIsMyMovie:
    def __init__(self, api_key):
        r = requests.get(API_URL, {'api_key': api_key})
        if r.status_code == 200:
            self.api_key = api_key
        else: raise ApiException('You API key is invalid.')

    def search(self, query):
        '''
            actually main function for calling API

            usage: search('your query')
            returns a Query objects
        '''
        r = self.search_helper(query)
        return Query(r, self)

    def search_helper(self, query, query_id=None):
        if not query or not len(query):
            raise ApiException('Query string can\'t be empty')
        if len(query) > 400:
            eprint('You query length exceeds 400 characters. It will be truncated.')
        params = {
            'api_key':      self.api_key,
            'text':         query[:400],
            'refinements':  'enabled',
            'query_id':     query_id
        }
        r = requests.get(API_URL, params)
        if r.status_code != 200:
            raise ApiException('Status Code: {}\nText: {}'.format(r.status_code, r.text))
        else:
            return json.loads(r.text)

class Query():
    '''
        Query object
          query.movies      # array of movies   (can be empty)
          query.id          # id of query       (not set if movies is empty)
          query.json        # the json response (useful for caching it)

          refine() method is for filtering inside the query
          it *modifies* the query object, doesn't return a new query
    '''
    def __init__(self, parsed_json, client):
        tmp = []
        if parsed_json != []:
            for m in parsed_json['results']:
                tmp.append(Movie(m))
            self.id = parsed_json['query_id']

        self.movies = tmp
        self.client = client
        self.json = parsed_json

    def refine(self, query):
        if not self.client: raise ApiException('This query cannot be refined. (Missing client instance)')
        r = WhatIsMyMovie.search_helper(self.client, query, query_id=self.id)
        self.id = r['query_id']
        tmp = []
        for m in parsed_json['results']:
            tmp.append(Movie(m))
        self.movies = tmp

    def __str__(self):
        return self.json

class ApiException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
