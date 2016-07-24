import csv
import requests

API_KEY = None
SECRET_KEY = None
ENDPOINT = None

def init(api_key, secret_key, endpoint='https://api.smyte.com'):
  global API_KEY, SECRET_KEY, ENDPOINT

  if API_KEY is not None:
    raise RuntimeError('init() already called')

  API_KEY = api_key
  SECRET_KEY = secret_key
  ENDPOINT = endpoint

def query(s, days=7):
  if API_KEY is None:
    raise RuntimeError('init() has not been called yet')

  f = requests.post(ENDPOINT + '/v2/smyteql', auth=(API_KEY, SECRET_KEY), data={
    'q': s,
    'numDays': days,
  })
  f.raise_for_status()

  return csv.DictReader(line.decode('utf-8') for line in f.iter_lines(decode_unicode=True))

__all__ = ('init', 'query')
