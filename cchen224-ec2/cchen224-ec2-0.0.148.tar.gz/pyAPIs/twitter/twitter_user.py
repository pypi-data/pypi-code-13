import json
import time
import traceback
from datetime import datetime

import tweepy
from cutils import ProgressBar


# INPUT_FILE = '/Volumes/cchen224/sb50/f_broncos'
# OUTPUT_FILE = '/Volumes/cchen224/sb50/u_broncos.json'
# with open(OUTPUT_FILE, 'r') as i:
#     read_uids = set([json.loads(line)['id'] for line in i])
#
#
# with open(INPUT_FILE, 'r') as i:
#     target_uids = set([int(line.strip()) for line in i])


def get_user(uids, account):

    auth = tweepy.OAuthHandler(account['consumer_key'], account['consumer_secret'])
    auth.set_access_token(account['access_key'], account['access_secret'])
    api = tweepy.API(auth)
    return api.lookup_users(user_ids=uids)


accounts = [
    {'consumer_key': 'YT0tutGIiNJPN1qgeTbeycyZN',
     'consumer_secret': '3kr7n4wcpSKbJMg2HdUYuv7z6u8Jx5hYeaxEeDunEs94FxRpQI',
     'access_key': '954798157-kSCkePC2Nh6c7XNTDpGBrRW602EG2AAGlxBO742z',
     'access_secret': 'LSDcRb7uMlkzDfmwXlzY7puddMfdBfU8te5cWgbb4S7Rv'},

    {'consumer_key': 'jtsyzmLZh8PVeDFpDESNFhbfx',
     'consumer_secret': 'yf8qgkfrgOnqsLpOgIYRRjXNkWZ9RMSIvizW0MyfdcaWF73GVo',
     'access_key': '4175032576-IEdW79v1rKvaOgySkwlv6px4o7UFYshwACzdaKw',
     'access_secret': 'm6Fs8MzOflylebJoC82Zp8PsO7gAYhJ5TB9OYDULRHdih'},

    {'consumer_key': 'b4cbNQ34QnKrWZisexzevVQ7v',
     'consumer_secret': 'gFvkcmVUgt6BMWgx3MgdMgjuXa1ZAWceR00retenOVowJB2PVz',
     'access_key': '3965724493-Uxnvo0YX9XoqAmaD2L25iO4jgrlzldJas5GPMXM',
     'access_secret': 'GoRdhfiXsEuErQ6ktGDrmXm9x22EdootO9trET9MEUQtG'},

    {'consumer_key': 'Iee46Dnt3iAeFnCyPSPvgA49f',
     'consumer_secret': 'Vkth3Ocia9CGCyfOY1TISuDN7FHIfytvViRsV3dGnYfqfEPKTD',
     'access_key': '4007054717-30wMpW7IfV8gjp1orx3QO0bePy6TvFc6536JM80',
     'access_secret': 'zD55I7EgcmIUzzZ7fM7ueljtMSCnIRNBCQdaVvbzDU5Vu'},

    {'consumer_key': 'bxzC2N7lVo3Zq5M7osbSA',
     'consumer_secret': 'mSkxIXbnWrtMwhLRAenqHiQek1cOLGYWbtOqRiN1g',
     'access_key': '323394874-rzrfdsG6MhpjGtMwd8oLGB0ylpGtXCAEFAV8WAH1',
     'access_secret': 'hgccGUbMea8xvwDMlhi746CZA41KmnGQdoU1lWfCO0'},

    {'consumer_key': 'Nao9qC3oYqwGfaLXz2N58A',
     'consumer_secret': 'Mb4D9tLI2vOkfcoISQ9XmAankVvHMjgeU3tIca57fg',
     'access_key': '5765972-CABSQQQJ5dAz17bhnfqDkngK6VdtDO22lJf4Np4Wyl',
     'access_secret': '6DlGbyVpesCTndcQNzQPaAUo413zB3d4tpZKik'},

    {'consumer_key': '1Djhi40YzfrYF2Ff2VHIg',
     'consumer_secret': 'beeGpNxnY5e6jvDF3eoDgpPjXNFUjUmBcVPmt4HI',
     'access_key': '5765972-CBYl6MfD72eQGqfBpq0rcxaLNOMCWc4rtSbmfw3n7U',
     'access_secret': '6QdcrCuk3pUfDfAQHpi6K4WDrEo8JN3Avjkm0CkJv0M'},

    {'consumer_key': 'bh8eEkSjVSJ5prg8zQFpvA',
     'consumer_secret': 'lf5Vgf8TEb1JsEIsNQ4ywiIXmzf1qKHjkEMQ7xa8PA',
     'access_key': '5765972-KHZdV1U14btxXQEb0XSLGuxcU26lv6J2vl2IvUDBY',
     'access_secret': 'nbfGzDOt0tuy5DRu5brM7JeKziXstkkOdeJcFkRtsE'},

    {'consumer_key': 'HTxksPmuHyg0QAMZAliNmNBmF',
     'consumer_secret': 'ghvtEvXgHvMgyof33ouzTVzIaPgpRUH8L2vSGXv5yCvaCCgf17',
     'access_key': '323394874-0IbdxFKF6zcH9Pn55oqqV4PEa4RhZR3ayZ3qc3fP',
     'access_secret': 'HAtoaQTBzyIcWP4Btbcp0PMksU1fb17nzladnSU793RjU'},

    {'consumer_key': 'AI3wfoBCQxgewAfLF5yvygKhA',
     'consumer_secret': 'KBB6jcgFW835uq1B7hh4jJ4TxINeggTlMwpqqkGpFxoiksasrT',
     'access_key': '323394874-qEwwWxJrMTSN5KlY5reOeunFvYtVEf9zyFY6r9TP',
     'access_secret': 'TuulKdzw8Mdx9k877GXOjJ25fuQnPFHvcCtNXWgu0tZiq'},

    {'consumer_key': '7VwQ2daz3p7JRn5EZxP6or3KA',
     'consumer_secret': 'FhFASS0XA9exDFc2K74Jji7JT85dfMev7aV1aN1Hg5sLnJZuX2',
     'access_key': '323394874-6KBVniBhB7xdTQISX0vG0zwfc4BWYKhyXfngrQpR',
     'access_secret': 'd0UZtdmZtFlu6yWJyp3Hh2ewlMZ4txoh9CLLiq2gxh9sW'},

]


uids = list(target_uids - read_uids)
with open(OUTPUT_FILE, 'a') as o:
    c = 0
    e = 0
    a = 0
    bar = ProgressBar(total=len(uids) / 100 + 1)
    while True:
        if e >= 5:
            print c
            break
        try:
            user_ids = uids[c:(c+100)]
            if not user_ids:
                break
            try:
                users = get_user(user_ids, accounts[a])
            except:
                a += 1
                a %= len(accounts)
                users = get_user(user_ids, accounts[a])
            [o.write(json.dumps(user._json).encode('utf-8') + '\n') for user in users]
            bar.move().log()
            c += 100
            e = 0
        except Exception, error:
            e += 1
            time.sleep(5)
            print datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            print error
