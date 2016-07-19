import csv
import json

BRANDS = ['Skittles',
          'Bud Light',
          'Advil',
          'Quicken',
          'Loans',
          'Acura',
          'Shock Top',
          'Taco Bell',
          'Marmot',
          'Squarespace',
          'Mountain Dew',
          'Audi',
          'Mobile Strike',
          'Hyundai',
          'PayPal',
          'Doritos',
          'SoFi',
          'Apartments',
          'Avocados From Mexico',
          'Avocados',
          'Snickers',
          'Michelob Ultra',
          'Pepsi',
          'Persil Proclean',
          'Toyota',
          'Coca-Cola',
          'OICisDifferent',
          'WeatherTech',
          'Dollar Shave Club',
          'T-Mobile',
          'TMobile',
          'Hyundai',
          'Buick',
          'Budweiser',
          'Honda',
          'Heinz',
          'Wix',
          'Fitbit',
          'Death Wish Coffee',
          'LG',
          'MINI USA',
          'MINI',
          'Pokemon',
          'Doritos',
          'TurboTax',
          'Jeep',
          'Amazon',
          'SunTrust',
          'Colgate',
          'Kia',
          'Axe',
          'Schick',
          '#StartStunning',
          '#Pokemon20',
          '#EveryDropCounts',
          '#GameDayStains',
          '#BaldwinBowl',
          '#MovinOnUp',
          '#Ballogize',
          '#GiveADamn',
          '#NotBackingDown',
          '#BestBuds',
          '#pepsihalftime',
          '#puppymonkeybaby',
          '#AvosInSpace',
          '#BolderThanBold',
          'MeetTheKetchups',
          '#DeclarationofDelicious',
          '#HyundaiSuperBowl',
          '#DefyLabels',
          '#AddPizzazz',
          '#GoPriusGo',
          '#TeamSmallBiz',
          '#onUp',
          '#SoFiGreat',
          '#RocketMortgage',
          '#EsuranceSweepstakes',
          '#CokeMini',
          'Jublia',
          'Mermot',
          'Machine Zone',
          'OIC',
          'Intel',
          'Bai',
          'Butterfinger',
          'Jack in the Box',
          'McDonalds',
          'Chrysler',
          'Intuit',
          'Esurance',
          'Quicken Loans',
          ]
BRANDS = list(set(BRANDS))

def get_follow_list(fp_in):
    with open(fp_in, 'r') as i:
        p = [line.strip() for line in i]
    return frozenset(p)


def merge_by_user(fp_in, fp_out, user_lst, **follower_list):
    import csv, json
    from datetime import datetime
    from datetime import timedelta
    from canalysis import get_sentiment
    from glob import glob
    import re

    t1 = datetime.strptime('2016-02-07 15:30:00', '%Y-%m-%d %H:%M:%S')
    t2 = datetime.strptime('2016-02-07 19:20:00', '%Y-%m-%d %H:%M:%S')


    users = dict()

    for file in glob(fp_in):
        with open(file, 'r') as i:
            if fp_in.endswith('.csv'):
                csvreader = csv.reader(i)
                for row in csvreader:
                    uid = row[0]
                    hashtags = set(row[5].split('|'))
                    emojis = row[8]
                    emojis = set(json.loads(row[8]).keys()) if emojis else set()

                    if uid not in users:
                        users[uid] = dict()
                        users[uid]['txt'] = row[4]
                        users[uid]['hst'] = hashtags
                        users[uid]['emj'] = emojis
                    else:
                        users[uid]['txt'] += ' ' + row[4]
                        users[uid]['hst'] |= hashtags
                        users[uid]['emj'] |= emojis

            elif fp_in.endswith('.json'):
                for line in i:
                    try:
                        jsontext = json.loads(line)
                        user = jsontext['user']
                    except:
                        continue

                    # tms = datetime.utcfromtimestamp(int(jsontext['timestamp_ms']) / 1000) - timedelta(hours=8)
                    # if tms > t2 or tms < t1:
                    #     continue

                    txt = jsontext['text'].encode('utf-8')
                    # if not re.compile('|'.join(BRANDS).lower()).search(txt.lower()):
                    #     continue

                    tid = jsontext['id_str']
                    uid = user['id_str']
                    scn = user['screen_name']

                    if uid not in user_lst:
                        continue

                    if uid in users:
                        users[uid]['txt'] += ' ' + txt
                        users[uid]['tid_count'] += 1
                    else:
                        users[uid] = dict()
                        users[uid]['txt'] = txt
                        users[uid]['tid_count'] = 1

    with open(fp_out, 'w') as o:
        csvwriter = csv.writer(o)
        for uid in users:
            follow = ''
            for team in follower_list:
                if uid in follower_list[team]:
                    follow = team
                    break
            users[uid]['follow'] = follow
            csvwriter.writerow([uid, follow, users[uid]['txt']])
    return users

p = get_follow_list('/Users/cchen224/Downloads/followers_panthers.txt')
b = get_follow_list('/Users/cchen224/Downloads/followers_broncos.txt')
pp = p - b
bb = b - p
bp = b & p
# merge_by_user('/Volumes/cchen224/sb50users.csv', '/Volumes/cchen224/sb50users_per_user.csv', broncos=bb, panthers=pp, both=bp)
# l = merge_by_user('/Volumes/cchen224/original/*.json', '/Volumes/cchen224/tweets_07_user_in_game.csv', user_list_ingame,broncos=bb, panthers=pp, both=bp)


def read_csv(fp_in, **y_label):
    import sys
    csv.field_size_limit(sys.maxsize)
    label = []
    text = []
    with open(fp_in, 'r') as i:
        csvreader = csv.reader(i)
        for row in csvreader:
            label.append(row[0])
            text.append(row[1])
    if y_label:
        label = [y_label[item] for item in label]
    return text, label

text, label = read_csv('/Volumes/cchen224/sb50_per_user_labeled.csv', both=0, broncos=1, panthers=2)


# from canalysis.ml_utilities import *
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.grid_search import GridSearchCV
from sklearn.linear_model import LogisticRegression, LassoCV
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.cross_validation import cross_val_score
from sklearn.svm import SVC
from sklearn.pipeline import FeatureUnion
from sklearn.externals import joblib
from datetime import datetime
from sklearn.feature_selection import SelectKBest, SelectFdr, chi2, SelectFromModel
import numpy as np


model = Pipeline([
    ('count', CountVectorizer(stop_words='english')),
    ('tfidf', TfidfTransformer()),
    # ('mnnbc', MultinomialNB()),
    ('select', SelectKBest(SelectFdr, k=1e5)),
    ('boosting', GradientBoostingClassifier(n_estimators=10000, learning_rate=1.0, max_depth=5, random_state=0)),
    # ('logit', LogisticRegression(multi_class='multinomial',solver='lbfgs'))
])
parameters = {'count__ngram_range': [(1, 1), (1, 2), (1,3)],
              'tfidf__use_idf': (True, False),
              # 'mnnbc__alpha': (1e-2, 1e-3, 1e-5, 1e-6),
              'boosting__max_depth': [1,2,3,4,5],
              }
# print 'Start', datetime.now().strftime('%H:%M:%S')
# gs_clf = GridSearchCV(model, parameters, n_jobs=-1, cv=10)
# gs_clf = gs_clf.fit(text, label)
# print gs_clf.best_score_
# print gs_clf.best_params_, '\n\n'
# print gs_clf.grid_scores_
# print datetime.now().strftime('%H:%M:%S')


model_logistic = Pipeline([
    ('count', CountVectorizer(stop_words='english', ngram_range=(1,2), min_df=2)),
    ('tfidf', TfidfTransformer(use_idf=True)),
    # ('select', SelectKBest(chi2, k=1e5)),
    ('logit', LogisticRegression(multi_class='multinomial',solver='lbfgs'))
])
scores = cross_val_score(model_logistic, text, label, cv=10)
model_logistic = model_logistic.fit(text, label)


# joblib.dump(gs_clf, '/Volumes/cchen224/boost.pkl', compress=9)
# with open('/Volumes/cchen224/tweets_07_in_game_preference.tsv', 'r') as i:
#     user_list_ingame = set([line.strip().split('\t')[0] for line in i])

def get_follower(fp_in, fp_out, model):
    users_pref = dict()
    uids = []
    txts = []
    switch_v = {0: 'both', 1: 'broncos', 2: 'panthers'}
    with open(fp_in, 'r') as i:
        csvreader = csv.reader(i)
        for row in csvreader:
            if row[1]:
                users_pref[row[0]] = row[1]
            else:
                # users_pref[row[0]] = switch_v[model.predict([row[2]])[0]] + '*'
                uids.append(row[0])
                txts.append(row[2])

    print 'Starting prediction'
    pred = [switch_v[item] + '*' for item in model.predict(txts)]
    users_pref.update(dict(zip(uids, pred)))

    print 'Starting output'
    with open(fp_out, 'w') as o:
        for uid in users_pref:
            o.write('\t'.join([uid, users_pref[uid]]) + '\n')
    return users_pref
user_pref = get_follower('/Volumes/cchen224/tweets_07_user_in_game.csv',
                         '/Volumes/cchen224/tweets_07_in_game_preference.tsv',
                         model_logistic)

with open('/Volumes/cchen224/tweets_07_in_game_preference.tsv', 'r') as i:
    user_pref = dict(map(lambda (uid, follow): (uid, follow), [uf.strip().split('\t')[0:2] for uf in i]))

def get_raw_csv(fp_in, fp_out, **follower_list):
    import csv, json
    from datetime import datetime
    from datetime import timedelta
    from canalysis import get_sentiment
    import re



def get_sentiment_wrt_game(fp_in, fp_out, cutoff, preference):
    import csv, json
    from datetime import datetime
    from datetime import timedelta
    from canalysis import get_sentiment
    from vaderSentiment.vaderSentiment import sentiment as vaderSentiment
    import re
    from glob import glob

    t1 = datetime.strptime('2016-02-07 15:30:00', '%Y-%m-%d %H:%M:%S')
    t2 = datetime.strptime('2016-02-07 19:20:00', '%Y-%m-%d %H:%M:%S')

    timeline_l = [datetime.strptime('2016/01/01 15:30', '%Y/%m/%d %H:%M'),
                  datetime.strptime('2016/02/07 15:44', '%Y/%m/%d %H:%M'),
                  datetime.strptime('2016/02/07 16:07', '%Y/%m/%d %H:%M'),
                  datetime.strptime('2016/02/07 16:26', '%Y/%m/%d %H:%M'),
                  datetime.strptime('2016/02/07 16:31', '%Y/%m/%d %H:%M'),
                  datetime.strptime('2016/02/07 17:45', '%Y/%m/%d %H:%M'),
                  datetime.strptime('2016/02/07 17:51', '%Y/%m/%d %H:%M'),
                  datetime.strptime('2016/02/07 18:00', '%Y/%m/%d %H:%M'),
                  datetime.strptime('2016/02/07 18:08', '%Y/%m/%d %H:%M'),
                  datetime.strptime('2016/02/07 18:33', '%Y/%m/%d %H:%M'),
                  datetime.strptime('2016/02/07 18:43', '%Y/%m/%d %H:%M'),
                  datetime.strptime('2016/02/07 19:05', '%Y/%m/%d %H:%M'),
                  datetime.strptime('2016/02/07 19:08', '%Y/%m/%d %H:%M'),
                  datetime.strptime('2016/05/07 19:08', '%Y/%m/%d %H:%M')]
    timeline_d_den = {(timeline_l[0], timeline_l[1]) : '1',
                      (timeline_l[1], timeline_l[3]) : '1.23',
                      (timeline_l[3], timeline_l[4]) : '-0.5',
                      (timeline_l[4], timeline_l[5]) : '0.44',
                      (timeline_l[5], timeline_l[9]) : '0.83',
                      (timeline_l[9], timeline_l[-1]) : '2'}
    timeline_d_car = {(timeline_l[0], timeline_l[1]) : '1',
                      (timeline_l[1], timeline_l[3]) : '-0.73',
                      (timeline_l[3], timeline_l[4]) : '1',
                      (timeline_l[4], timeline_l[5]) : '-0.44',
                      (timeline_l[5], timeline_l[9]) : '-0.83',
                      (timeline_l[9], timeline_l[-1]) : '-2'}

    switch = {'both': 0, 'broncos': 1, 'panthers': 2}
    switch_v = {0: 'both', 1: 'broncos', 2: 'panthers'}

    facial = re.sub('(\#|\$|\(|\)|\[|\]|\?|\:|\*|\-|\\\\|\>|\<|\{|\})', '\ \\1', '|'.join(face.keys()))
    facial = re.sub(' ', '', facial)
    pattern10 = re.compile(r'(' + facial + r')')
    pattern11 = re.compile(r'(' + '|'.join(emoji_sent.keys()) + r')')
    pattern2 = re.compile(r'\b(' + '|'.join(illformed.keys()) + r')\b')
    pattern3 = re.compile('|'.join(BRANDS).lower())


    with open(fp_out, 'w') as o:
        csvwriter = csv.writer(o)
        csvwriter.writerow(['user_id','screen_name','tweet_id','timestamp','text','mentioned_brands','follow','sentiment_wrt_text','sentiment_wrt_game'])

        for file in glob(fp_in):
            with open(file, 'r') as i:
                if fp_in.endswith('.json'):
                    for line in i:
                        try:
                            jsontext = json.loads(line)
                            user = jsontext['user']
                        except:
                            continue

                        tms = datetime.utcfromtimestamp(int(jsontext['timestamp_ms']) / 1000) - timedelta(hours=8)
                        if tms > t2 or tms < t1:
                            # print tms.strftime('%H:%M:%S')
                            continue

                        txt = re.sub('\n' , ' ' , jsontext['text'])
                        txt = re.sub(' +', ' ', txt)
                        txt = pattern2.sub(lambda x: illformed[x.group()], txt)
                        txt = re.sub('http.+$', '', txt)

                        if pattern3.search(txt.lower()):
                            ads = '|'.join(pattern3.findall(txt.lower()))
                        else:
                            continue

                        tid = jsontext['id_str']
                        uid = user['id_str']
                        scn = user['screen_name']

                        snt = vaderSentiment(txt.encode('utf-8'))['compound']

                        txt_e = pattern11.sub(lambda x: str([[emoji_sent.get(x.group())]]), txt)
                        txt_e = pattern10.sub(lambda x: str([[face.get(x.group())]]), txt_e)
                        es = [float(item) for item in re.findall("\[\[([0-9.]*?)\]\]", txt_e) if item != 'None']
                        snt_e = sum(es) + snt


                        if snt_e < -1 * cutoff:
                            snt_e = 'neg'
                        elif snt_e > cutoff:
                            snt_e = 'pos'
                        else:
                            snt_e = 'neu'

                        follow = preference.get(uid, '')
                        if not follow:
                            print 'uid not found in preference.'
                            continue

                        sent_game = ''
                        for interval in timeline_d_den:
                            if interval[0] <= tms < interval[1]:
                                if re.sub('\*', '', follow) == 'broncos':
                                    sent_game = timeline_d_den[interval]
                                elif re.sub('\*', '', follow) == 'panthers':
                                    sent_game = timeline_d_car[interval]
                                else:
                                    sent_game = '0'
                        csvwriter.writerow([uid, scn, tid, tms.strftime('%Y-%m-%d %H:%M:%S'), txt.encode('utf-8'), ads, follow, snt_e, sent_game])
        # csvreader = csv.reader(i)
        # for row in csvreader:
get_sentiment_wrt_game('/Volumes/cchen224/original/tweets_0[6-7].json',
                       '/Volumes/cchen224/tweets_in_game_sentiment_update5.0.csv',
                       0.1,
                       user_pref)

with open('/Users/cchen224/Downloads/followers_panthers.txt', 'r') as i:
    p = [line.strip() for line in i]
    p = frozenset(p)

with open('/Users/cchen224/Downloads/followers_broncos.txt', 'r') as i:
    b = [line.strip() for line in i]
    b = frozenset(b)


pp_ = p - b
bb_ = b - p
bp_ = b & p






#############
from sklearn.cross_validation import KFold
for train_index, test_index in KFold(n=len(text), n_folds=10, shuffle=True, random_state=0):
    X_train, X_test = np.array(text)[train_index], np.array(text)[test_index]
    y_train, y_test = np.array(label)[train_index], np.array(label)[test_index]
    break

model = Pipeline([
    ('count', CountVectorizer(stop_words='english', ngram_range=(1,2), min_df=2)),
    ('tfidf', TfidfTransformer()),
    # ('mnnbc', MultinomialNB()),
    # ('select', SelectKBest(SelectFdr, k=1e5)),
    # ('boosting', GradientBoostingClassifier(n_estimators=10000, learning_rate=1.0, max_depth=5, random_state=0)),
    # ('logit', LogisticRegression(multi_class='multinomial',solver='lbfgs'))
])
X_train = model.fit_transform(X_train)
X_test = model.fit_transform(X_test)

# X_train = DenseTransformer.fit_transform(X_train)
# X_test = DenseTransformer.fit_transform(X_test)

boosting = GradientBoostingClassifier(n_estimators=10000, learning_rate=1.0, max_depth=5, random_state=0)
boosting = boosting.fit(X_train, y_train)


with open('/Users/cchen224/Downloads/data/corpus.v1.2.tweet', 'r') as i:
    illformed = dict()
    csvreader = csv.reader(i, delimiter='\t')
    for row in csvreader:
        if len(row) == 3 and row[1] == 'OOV':
            illformed[row[0]] = row[2]




cutoff = 0.1
with open('/Volumes/cchen224/tweets_07_sentiment_text_only.csv', 'w') as o:
    import csv, json
    from datetime import datetime
    from datetime import timedelta
    from canalysis import get_sentiment
    import re
    import emoji
    from vaderSentiment.vaderSentiment import sentiment as vaderSentiment
    csvwriter = csv.writer(o)
    facial = re.sub('(\#|\$|\(|\)|\[|\]|\?|\:|\*|\-|\\\\|\>|\<|\{|\})', '\ \\1', '|'.join(emoji_sent.keys()))
    facial = re.sub(' ', '', facial)
    pattern1 = re.compile(r'(' + facial + r')')
    pattern2 = re.compile(r'\b(' + '|'.join(illformed.keys()) + r')\b')


    with open('/Volumes/cchen224/tweets_07.json', 'r') as i:


        t1 = datetime.strptime('2016-02-07 15:30:00', '%Y-%m-%d %H:%M:%S')
        t2 = datetime.strptime('2016-02-07 19:20:00', '%Y-%m-%d %H:%M:%S')
        for line in i:
            try:
                jsontext = json.loads(line)
                user = jsontext['user']
            except:
                continue

            tms = datetime.utcfromtimestamp(int(jsontext['timestamp_ms']) / 1000) - timedelta(hours=8)
            if tms > t2 or tms < t1:
                continue

            txt = re.sub('\n' , ' ' , jsontext['text'])
            txt = pattern2.sub(lambda x: illformed[x.group()], txt)
            txt = re.sub('http.+$', '', txt)

            snt = vaderSentiment(txt.encode('utf-8'))['compound']

            txt_e = pattern1.sub(lambda x: str([[emoji_sent.get(x.group())]]), txt)
            es = [float(item) for item in re.findall("\[\[([0-9.]*?)\]\]", txt_e) if item != 'None']
            snt_e = sum(es) + snt

            if snt < -1 * cutoff:
                snt = 'neg'
            elif snt > cutoff:
                snt = 'pos'
            else:
                snt = 'neu'

            if snt_e < -1 * cutoff:
                snt_e = 'neg'
            elif snt_e > cutoff:
                snt_e = 'pos'
            else:
                snt_e = 'neu'
            csvwriter.writerow([snt, snt_e, txt.encode('utf-8')])


import math
def normalize(score, alpha=15):
    # normalize the score to be between -1 and 1 using an alpha that approximates the max expected value
    normScore = score/math.sqrt( ((score*score) + alpha) )
    return normScore


with open('/Volumes/cchen224/tweets_07_in_game_preference.tsv', 'r') as i:
    csvreader = csv.reader(i, delimiter='\t')
    users = set()
    tweets = set()
    for row in csvreader:
        users.add(row[0])
        tweets.add(row[1])
len(users)


def get_adjs(text):
    import nltk
    nltk_splitter = nltk.data.load('tokenizers/punkt/english.pickle')
    nltk_tokenizer = nltk.tokenize.TreebankWordTokenizer()
    sentences = nltk_splitter.tokenize(text)
    tokenized_sentences = [nltk_tokenizer.tokenize(sent) for sent in sentences]
    pos = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
    jjs = [' '.join([word[0] for word in words if 'JJ' in word[1]]) for words in pos]
    return ' '.join(jjs)


with open('/Volumes/cchen224/tweets_in_game_user.csv', 'w') as o:
    for file in glob('/Volumes/cchen224/p/*.csv'):
        with open(file, 'r') as i:
            [o.write(line.strip() + '\n') for line in i]

from datetime import datetime
timeline_b_ = [datetime.strptime('2016/01/01 15:30', '%Y/%m/%d %H:%M'),
               datetime.strptime('2016/02/07 16:26', '%Y/%m/%d %H:%M'),
               datetime.strptime('2016/02/07 17:33', '%Y/%m/%d %H:%M'),
               datetime.strptime('2016/02/07 17:45', '%Y/%m/%d %H:%M'),
               datetime.strptime('2016/02/07 18:33', '%Y/%m/%d %H:%M'),
               datetime.strptime('2016/02/07 19:21', '%Y/%m/%d %H:%M')]
timeline_b = {(timeline_b_[0], timeline_b_[1]) : 1,
              (timeline_b_[1], timeline_b_[2]) : 2,
              (timeline_b_[2], timeline_b_[3]) : 2.5,
              (timeline_b_[3], timeline_b_[4]) : 3,
              (timeline_b_[4], timeline_b_[5]) : 4,}


from glob import glob
import re
import csv
with open('/Volumes/cchen224/tweets_in_game_users.csv', 'r') as i:
    csvreader = csv.reader(i)
    users = dict(map(lambda (user_id, is_verified, bio, location, join_date, tweets, following, followers, likes):
                     (user_id, [is_verified, bio, location, join_date, tweets, following, followers, likes]),
                     (row for row in csvreader)))
with open('/Volumes/cchen224/tweets_in_game_hashtags.csv', 'r') as i:
    brands_hashtags = dict(map(lambda (x, y): (x.lower(), y), (line.strip().split(',') for line in i)))
with open('/Volumes/cchen224/tweets_in_game_ads_labels_update2.csv', 'r') as i:
    brands_emotions = dict()
    brands_appearance = dict()
    for line in i:
        if line.startswith('#'):
            continue
        tokens = line.strip().split(',')
        ad = tokens[0].lower()
        if ad not in brands_emotions:
            brands_emotions[ad] = [tokens[2:10]]
            brands_appearance[ad] = [2.5 if tokens[10] == 'halftime' else int(tokens[10])]
        else:
            brands_emotions[ad].append(tokens[2:10])
            brands_appearance[ad].append(2.5 if tokens[10] == 'halftime' else int(tokens[10]))

        if tokens[1]:
            ad = tokens[1].lower()
            if ad not in brands_emotions:
                brands_emotions[ad] = [tokens[2:10]]
                brands_appearance[ad] = [2.5 if tokens[10] == 'halftime' else int(tokens[10])]
            else:
                brands_emotions[ad].append(tokens[2:10])
                brands_appearance[ad].append(2.5 if tokens[10] == 'halftime' else int(tokens[10]))

with open('/Volumes/cchen224/tweets_in_game_sentiment_update5.0.csv', 'r') as i:
    csvreader = csv.reader(i)
    with open('/Volumes/cchen224/tweets_in_game_sentiment_update5.1.csv', 'w') as o:
        csvwriter = csv.writer(o)
        csvwriter.writerow(['#user_id', 'screen_name', 'tweet_id', 'timestamp', 'text', 'mentioned_brands',
                            'follow', 'sentiment_wrt_text', 'sentiment_wrt_game',
                            'is_verified', 'bio', 'location', 'join_date',
                            'n_tweets', 'n_following', 'n_followers', 'n_likes',
                            'apprearence (which quarter)',
                            'anger','fear','anticipation','surprise','joy','sadness','trust','disgust',
                            'ad_pos', 'ad_neg'])
        for row in csvreader:
            notfound = False
            quarter = None
            if row[0].startswith('#'):
                continue
            uinfo = users.get(row[1])
            if not uinfo: continue
            row.extend(uinfo)  # , ['', '', '', '', '', '', '', '']
            # brand_hashtag = [brands_appearance.get(brand, '') for brand in row[5].split('|') if '#' in brand]
            brand_hashtags = [brand for brand in row[5].split('|') if '#' in brand]
            try:
                brand_hashtag = brand_hashtags[0]
            except:
                brand_hashtag = brand_hashtags
                pass
            if brand_hashtag:
                emotions = ''
                for brand_hashtag in brand_hashtags:
                    emotions = brands_emotions.get(brand_hashtag, '')
                    if emotions:
                        break

                if not emotions:
                    if not [b for b in row[5].split('|') if not b.startswith('#')]:
                        notfound = True
                        continue

                    brand_emotion = ['','','','','','','','',]
                elif len(emotions) == 1:
                    quarter = brands_appearance[brand_hashtag][0]
                    brand_emotion = emotions[0]
                else:
                    tms = datetime.strptime(row[3], '%Y-%m-%d %H:%M:%S')
                    for time_interval in timeline_b:
                        if time_interval[0] <= tms < time_interval[1]:
                            quarter = timeline_b[time_interval]
                            break
                    if quarter not in brands_appearance[brand_hashtag]:
                        appearance = brands_appearance[brand_hashtag]
                        quarter = max(appearance) if quarter > max(appearance) else min(appearance)
                    brand_emotion = emotions[brands_appearance[brand_hashtag].index(quarter)]

            brands = [brand for brand in row[5].split('|') if not brand.startswith('#')]
            if not notfound and brands and not quarter:  # 2016-02-07 15:30:00

                brand_hashtag = ''
                # brands = [brand for brand in row[5].split('|') if not brand.startswith('#')]
                for brand in brands:
                    brand_hashtag = brands_appearance.get(brand, '')
                    if brand_hashtag:
                        brand_hashtag = brand
                        break

                if not brand_hashtag:
                    quarter = 0
                    brand_emotion = ['','','','','','','','',]
                    continue


                elif len(brands_emotions[brand_hashtag]) == 1:
                    quarter = brands_appearance[brand_hashtag][0]
                    brand_emotion = brands_emotions[brand_hashtag][0]
                else:
                    tms = datetime.strptime(row[3], '%Y-%m-%d %H:%M:%S')
                    for time_interval in timeline_b:
                        if time_interval[0] <= tms < time_interval[1]:
                            quarter = timeline_b[time_interval]
                            break
                    if quarter not in brands_appearance[brand_hashtag]:
                        appearance = brands_appearance[brand_hashtag]
                        quarter = max(appearance) if quarter > max(appearance) else min(appearance)
                    brand_emotion = brands_emotions[brand_hashtag][brands_appearance[brand_hashtag].index(quarter)]
                        # quarter = min([min(appearance, quarter) for appearance in brands_appearance[brand_hashtag]])
                # brand_hashtag = min(float(brands_appearance(row[5].split('|')[0])), float(brand_hashtag))

            if quarter == 2.5:
                row.append('halftime')
            elif notfound:
                row.append(99)
            else:
                row.append(quarter)
            row.extend(brand_emotion)
            brand_emotion_pos = sum([int(item) for counter, item in enumerate(brand_emotion)
                                     if counter in [2,3,4,6] and item])
            brand_emotion_neg = sum([int(item) for counter, item in enumerate(brand_emotion)
                                     if counter in [0,1,5,7] and item])
            row.append(brand_emotion_pos)
            row.append(brand_emotion_neg)
            csvwriter.writerow(row)


import csv
with open('/Volumes/cchen224/tweets_in_game_sentiment_update7.1.csv', 'r') as i:
    csvreader = csv.reader(i)
    head = csvreader.next()
    lines = [line for line in csvreader]
header = head[:7]
header.extend(['sentiment_wrt_text_p', 'sentiment_wrt_text_0.03', 'sentiment_wrt_text_0.05', 'sentiment_wrt_text_0.1', 'sentiment_wrt_text_vader',
               'sentiment_wrt_game_p', 'sentiment_wrt_game', #'sentiment_wrt_game_old',
               'sentiment_wrt_game_by_quarter'])
header.extend(head[9:])

def get_sent(value, cutoff):
    value = float(value)
    if value > cutoff:
        return 'pos'
    elif value < cutoff * -1:
        return 'neg'
    else:
        return 'neu'

with open('/Volumes/cchen224/tweets_in_game_sentiment_update5.0.csv', 'r') as i:
    csvreader = csv.reader(i)
    tid_sent = dict()
    for row in csvreader:
        if row[0].startswith('#'): continue
        tid_sent[row[2]] = row[7]

with open('/Volumes/cchen224/tweets_in_game_sentiment_update4.csv', 'r') as i:
    csvreader = csv.reader(i)
    tid_sent_game_old = dict()
    for row in csvreader:
        if row[0].startswith('#'): continue
        tid_sent_game_old[row[2]] = row[8]

from datetime import datetime
import re
timeline_l = [datetime.strptime('2016/01/01 15:30', '%Y/%m/%d %H:%M'),
              datetime.strptime('2016/02/07 15:44', '%Y/%m/%d %H:%M'),
              datetime.strptime('2016/02/07 16:07', '%Y/%m/%d %H:%M'),
              datetime.strptime('2016/02/07 16:26', '%Y/%m/%d %H:%M'),
              datetime.strptime('2016/02/07 16:31', '%Y/%m/%d %H:%M'),
              datetime.strptime('2016/02/07 17:45', '%Y/%m/%d %H:%M'),
              datetime.strptime('2016/02/07 17:51', '%Y/%m/%d %H:%M'),
              datetime.strptime('2016/02/07 18:00', '%Y/%m/%d %H:%M'),
              datetime.strptime('2016/02/07 18:08', '%Y/%m/%d %H:%M'),
              datetime.strptime('2016/02/07 18:33', '%Y/%m/%d %H:%M'),
              datetime.strptime('2016/02/07 18:43', '%Y/%m/%d %H:%M'),
              datetime.strptime('2016/02/07 19:05', '%Y/%m/%d %H:%M'),
              datetime.strptime('2016/02/07 19:08', '%Y/%m/%d %H:%M'),
              datetime.strptime('2016/05/07 19:08', '%Y/%m/%d %H:%M')]
timeline_d_den = {(timeline_l[0], timeline_l[1]) : '1',
                  (timeline_l[1], timeline_l[3]) : '0.23',
                  (timeline_l[3], timeline_l[5]) : '0.3',
                  (timeline_l[5], timeline_l[9]) : '0.83',
                  (timeline_l[9], timeline_l[-1]) : '1.14'}
timeline_d_car = {(timeline_l[0], timeline_l[1]) : '1',
                  (timeline_l[1], timeline_l[3]) : '-0.23',
                  (timeline_l[3], timeline_l[5]) : '-0.2',
                  (timeline_l[5], timeline_l[9]) : '-0.83',
                  (timeline_l[9], timeline_l[-1]) : '-1'}


with open('/Volumes/cchen224/tweets_in_game_sentiment_update8.csv', 'w') as o:
    csvwriter = csv.writer(o)
    csvwriter.writerow(header)
    for row in lines:
        tms = datetime.strptime(row[3], '%Y-%m-%d %H:%M:%S')
        follow = row[6]
        for interval in timeline_d_den:
            if interval[0] <= tms < interval[1]:
                if re.sub('\*', '', follow) == 'broncos':
                    sent_game = timeline_d_den[interval]
                elif re.sub('\*', '', follow) == 'panthers':
                    sent_game = timeline_d_car[interval]
                else:
                    sent_game = '0'
        out = row[:7]
        out.extend([row[7], get_sent(row[7], 0.03), get_sent(row[7], 0.05), get_sent(row[7], 0.1), tid_sent[row[2]],
                   row[8], get_sent(row[8], 0.) if row[8] != '1' else 'neu',
                        get_sent(sent_game, 0.) if sent_game != '1' else 'neu'])
        out.extend(row[9:])
        # row.insert(8, get_sent(row[7], 0.1))
        # row.insert(10, get_sent(row[9], 0) if row[9] != '1' else 'neu')
        # row.insert(9, tid_sent[row[2]])
        # row.insert(11, tid_sent_game_old[row[2]])

        csvwriter.writerow(out)

with open('/Volumes/cchen224/tweets_in_game_sentiment_update6_i_vs_j.csv', 'w') as o:
    csvwriter = csv.writer(o)
    with open('/Volumes/cchen224/tweets_in_game_sentiment_update6_0.05.csv', 'r') as i:
        csvreader = csv.reader(i)
        csvreader.next()
        for row in csvreader:
            if row[8] != row[9]:
                if 'neu' not in [row[8], row[9]]:
                    csvwriter.writerow([row[2], row[4], row[8], row[9]])






from glob import glob
tweets = []
for file in glob('/Users/cchen224/Downloads/expended_thread_aws/*.csv.txt'):
    with open(file, 'r') as i:
        brand = re.sub('^@|[.]csv[.]txt$', '', file.split('/')[-1])
        csvreader = csv.reader(i, delimiter='\t')
        is_use = True
        for row in csvreader:
            if is_use:
                tweets.append([brand, row[0], row[1], re.sub('\n|\r', ' ', row[3])])
                is_use = False
            elif not row:
                is_use = True

tweets = [tweet for tweet in tweets if not re.compile(tweet[0].lower()).search(tweet[3].lower())]

with open('/Volumes/cchen224/amazon_aws_brands.csv', 'w') as o:
    csvwriter = csv.writer(o)
#
#
#
# import praw
# import webbrowser
# import re
# r = praw.Reddit(user_agent='ccTest')
# r.set_oauth_app_info(client_id='FdkfxBHQeKNfaQ',
#                      client_secret='7U1mGVNkuHfQ2nU21MeVSWA5xOs',
#                      redirect_uri='http://127.0.0.1:65010/authorize_callback')
# url = r.get_authorize_url('uniqueKey', 'read', True)
# webbrowser.open(url)
# access_information = r.get_access_information('VtiF9ev2b8qVsSs5UQmH4ubX294') # use token after "code =" in url
# r.set_access_credentials(**access_information)
# subreddit = r.get_subreddit('SuicideWatch')
# submissions = [submission for submission in subreddit.get_hot(limit=9999999)]
#
#
#
# import re
# import csv
#
#
# def parse_comments(comment):
#     title = comment.title if hasattr(comment, 'title') else ''
#     author_name = comment.author.name if comment.author else ''
#     author_id = comment.author.id if comment.author else ''
#     parent_id = comment.parent_id if hasattr(comment, 'parent_id') else ''
#     parent_id = re.sub('t[0-9]\\_', '', parent_id)
#     post_id = comment.id
#     post_text = comment.body.encode('utf-8') if hasattr(comment, 'body') else comment.selftext.encode('utf-8')
#     post_text = re.sub('\n|\r', ' ', post_text)
#     voteups = comment.ups
#     votedowns = comment.downs
#     timestamp = int(comment.created_utc)
#     out = [[title, author_name, author_id, post_id, parent_id, timestamp, post_text, voteups, votedowns, ]]
#
#     replies = comment.comments if hasattr(comment, 'comments') else comment.replies
#     if replies:
#         for reply in replies:
#             out.extend(parse_comments(reply))
#         return out
#     else:
#         return out
#
#
# with open('/Users/cchen224/Downloads/reddit.csv', 'w') as o:
#     csvwriter = csv.writer(o)
#     csvwriter.writerow(['title',
#                         'author_name', 'author_id', 'post_id', 'parent_id',
#                         'timestamp', 'post_text', 'voteups', 'votedowns',])
#     for submission in submissions:
#         [csvwriter.writerow(item) for item in parse_comments(submission)]
