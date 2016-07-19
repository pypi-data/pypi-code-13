import time

import tweepy


def get_followers_ids(user_id, account):

    auth = tweepy.OAuthHandler(account['consumer_key'], account['consumer_secret'])
    auth.set_access_token(account['access_key'], account['access_secret'])
    api = tweepy.API(auth)

    # f = open(user_id + '_followings.txt', 'w+')
    current_page = 1
    user_timeline = tweepy.Cursor(api.user_timeline, user_id=user_id, since_id=696163960001679361, max_id=None, lang='en').pages()
    # user_timeline = tweepy.Cursor(api.user_timeline, screen_name=user_id, lang='en').pages()
    # print 'Starting collect ' + screen_name
    while True:
        try:
            print '\tGetting page ' + str(current_page)
            ids = user_timeline.next()
            # for i in ids:
                # f.write(str(i) + '\n')
            current_page += 1
            time.sleep(60)
        except tweepy.TweepError:
            print '\tWaiting on rate limit.'
            time.sleep(60)
        except StopIteration:
            # print screen_name + ' Done!\n\n\n'
            break
    f.close()


# import json
# f = open('/Users/cchen224/Downloads/tweets_07.json')
# file = json.load(f)
# 
#
#
# user_id=2634592777
#
# import time
# from tweepy.error import TweepError
# with open('/Users/cchen224/Downloads/brandlist.txt', 'r') as i:
#     users = [line.strip() for line in i]
# # geo = dict()
# # with open('/Users/cchen224/Downloads/brandlist.geo', 'w') as o:
#     for user_id in users:
#         if user_id not in geo:# and user_id not in ['suncelltweets', 'Mobilink', 'BeatsMusicHelp', 'ShawDirect_News']:
#             print user_id
#             try:
#                 geo[user_id] = tweepy.Cursor(api.user_timeline, screen_name=user_id, lang='en').pages().next()[0]._json['user']['time_zone']
#                 # time.sleep(5)
#             except TweepError, e:
#                 pass
#             except StopIteration:
#                 pass
#
# with open('/Users/cchen224/Downloads/brandlist.geo', 'w') as o:
#     [o.write('\t'.join([key, geo[key]]) + '\n') for key in geo if geo[key]]
#
