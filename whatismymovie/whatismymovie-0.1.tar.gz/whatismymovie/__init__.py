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
        return Query(r[0], r[1], self)

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
            result = []
            tmp = json.loads(r.text)
            for m in tmp['results']:
                result.append(Movie(m))
            return (tmp['query_id'], result)

class Query():
    '''
        Query object
          query.movies      # array of movies
          query.id          # id of query

          refine() method is for filtering inside the query
          it *modifies* the query object, doesn't return a new query
    '''
    def __init__(self, id, movies, client):
        self.id = id
        self.movies = movies
        self.client = client

    def refine(self, query):
        r = WhatIsMyMovie.search_helper(self.client, query, query_id=self.id)
        self.id = r[0]
        self.movies = r[1]

class ApiException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
