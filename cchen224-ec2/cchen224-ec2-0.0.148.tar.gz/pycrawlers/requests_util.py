import requests


class RequestsUtil:

    def __init__(self, max_retries=10, header=None):
        self.session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(max_retries=max_retries)
        self.session.mount('https://', adapter)
        self.header = header

    def get(self, url, timeout=60):
        return self.session.get(url, headers=self.header, timeout=timeout)



# import csv
# with open('/Volumes/cchen224/sb50/mappingback.csv', 'r') as i:
#     csvreader = csv.reader(i)
#     mapping = dict(map(lambda (x, y): (x.lower(), y.lower()), (row for row in csvreader)))
# with open('/Volumes/cchen224/sb50/tweets_in_game_sentiment_update6_0.1.csv', 'r') as i:
#     csvreader = csv.reader(i)
#     next(csvreader)
#     out = []
#     for row in csvreader:
#         brands = set()
#         for item in row[5].split('|'):
#             brands.add(mapping[item])
#         if 'pepsi' in brands and 'doritos' in brands:
#             brands.remove('pepsi')
#         if 'pepsi' in brands and 'mountain dew' in brands:
#             brands.remove('pepsi')
#         if '' in brands and len(brands) > 1:
#             brands.remove('')
#         if '' in brands and len(brands) == 1:
#             out.append('@_@')
#         else:
#             out.append('|'.join(brands))
#
# with open('/Volumes/cchen224/sb50/tweets_in_game_sentiment_update6_0.1_mentions.csv', 'w') as o:
#     [o.write(item + '\n') for item in out]