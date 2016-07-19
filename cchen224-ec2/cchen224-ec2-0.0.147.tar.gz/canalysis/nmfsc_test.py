import csv
import pickle
import re
from glob import glob

import matlab.engine
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.decomposition import NMF
from sklearn.pipeline import Pipeline
import os.path
from datetime import datetime

from CMUTweetTagger import runtagger_parse

STOPWORDS = ENGLISH_STOP_WORDS.union(['hi', 'just'])

# eng = matlab.engine.start_matlab()




# PATTERN = re.compile('(\\@|http(s|)\\:\\/\\/|pic\\.twitter\\.com)\S+')
INCLUDE = dict(map(lambda x: (x, ''), ['V', 'N', 'A', 'R', '!', 'U', 'G', 'D', '^', 'T', '#', 'S', 'Z', 'L', 'E', '$']))
file_counter = 0
for file in sorted(glob('/Volumes/cchen224/brand_threads/input_0615/*.csv.txt'), key=os.path.getsize)[::-1]:
    file_counter += 1
    print '\n\n\n' + str(file_counter) + '.',
    brand_name = file.split('/')[-1][:-8]
    print brand_name, datetime.now().strftime('%H:%M:%S')

    for type in ['brand', 'user']:
        print '\ngetting data...',
        t0 = datetime.now()
        tweets = []
        tttttt = []
        with open(file, 'r') as i:
            csvreader = csv.reader(i, delimiter='\t')
            posters = dict()
            uids = []
            tids = []
            for row in csvreader:
                if row:
                    poster = row[2]
                    uids.append(poster)
                    tids.append(row[1])
                    text = re.sub('/n|/r', ' ', row[3].strip())
                    if type == 'brand':
                        if poster not in posters:
                            posters[poster] = text
                        else:
                            posters[poster] += '. ' + text
                    if type == 'user':
                        if poster not in posters:
                            posters[poster] = text

                else:
                    # if (len(posters) == 2 and brand_name in posters) or (len(posters) == 1):
                    #     for poster in posters:
                    #         # tweets.append(PATTERN.sub(' ', posters[poster]))
                    #         tweets.append(posters[poster])


                    # brand only agreigte
                    if uids[0] != brand_name:
                        if type == 'brand':
                            if (brand_name in posters and len(posters) == 2):
                                for poster in posters:
                                    if brand_name == poster:
                                        if posters[poster]:
                                            tweets.append(posters[poster])
                                            tttttt.append(tids[0])

                        # user only
                        if type == 'user':
                            if (brand_name in posters and len(posters) == 2):# or (brand_name not in posters and len(posters) == 1):
                                # tweets.append(PATTERN.sub(' ', posters[poster]))
                                for poster in posters:
                                    if poster != brand_name:
                                        if posters[poster]:
                                            tweets.append(posters[poster])
                                            tttttt.append(tids[0])
                    posters = dict()
                    uids = []
                    tids = []
        print 'done'

        print 'postagging...',
        postags = runtagger_parse(tweets)
        tweets_p = [' '.join([token[0].split('/')[-1] for token in tweet if token[1] in INCLUDE]) for tweet in postags]
        tweets_p = [re.sub('([0-9])[\\(|\\)|\\-|\\+]([0-9])', '\\1\\2', item) for item in tweets_p]
        print 'done'

        # for file in glob('/Volumes/cchen224/brand_threads/expended_thread_aws/@2KSupport.csv.txt'):
        #     with open(file, 'r') as i:
        #         doc_index.append(file.split('/')[-1])
        #         tweets.append(re.sub('(\\@|http(s|)\\:\\/\\/|pic\\.twitter\\.com)\S+', '', i.next()).strip())

        model = Pipeline([
            ('wc', CountVectorizer(stop_words=STOPWORDS)),
            ('tfidf', TfidfTransformer(use_idf=True))
        ])

        print 'tfidf convertion...',
        tfidf = model.fit_transform(tweets_p)
        # tfidf_d = tfidf.todense().tolist()
        # tfidf_m = matlab.double(tfidf_d)
        print tfidf.shape, 'done'

        # print 'nmf...',
        # W, H = eng.nmfsc(tfidf_m, 10., 0.5, 0.2, 'out', False, nargout=2)
        # print 'done'
        #
        #
        # W = [list(line) for line in W]
        # H = [list(line) for line in H]

        vocab = model.steps[0][1].vocabulary_
        vocab_= dict((v, k) for k, v in vocab.iteritems())

        print 'saving matrices...',
        # with open(file[:-8] + '_' + type + '_W.data', 'w') as o:
        #     pickle.dump(W, o)
        # with open(file[:-8] + '_' + type + '_H.data', 'w') as o:
        #     pickle.dump(H, o)
        with open(file[:-8] + '_' + type + '_V.data', 'w') as o:
            pickle.dump(tfidf, o)
        with open(file[:-8] + '_' + type + '_vocab.data', 'w') as o:
            pickle.dump(vocab_, o)
        with open(file[:-8] + '_' + type + '_docs.data', 'w') as o:
            pickle.dump(tweets, o)
        with open(file[:-8] + '_' + type + '_stats.data', 'w') as o:
            o.write(str(tfidf.shape))
            # pickle.dump(tfidf.shape, o)
        with open(file[:-8] + '_' + type + '_tids.data', 'w') as o:
            pickle.dump(tttttt, o)
        print 'done'
        print (datetime.now() - t0).seconds


        # import numpy as np
        # print type, ':'
        # for counter, topic in enumerate(H):
        #     print 'Topic' + str(counter) + ':',
        #     for index in np.array(topic).argsort()[-10:][::-1]:
        #         print vocab_[index],
        #     print
        #
        # for counter, topic in enumerate(W):
        #     # print 'Topic' + str(counter) + ':',
        #     print tweets[counter]
        #     for index in np.array(topic).argsort()[-5:][::-1]:
        #         print '\t', index, np.array(topic)[index]
        #     print



# eng.quit()


################################################################################################
import pickle
import numpy as np
H_cutoff = 0.2
with open('/Volumes/cchen224/brand_threads/input_0615/2ksupport_user_H.data', 'r') as i:
    H = np.array(pickle.load(i))
topics = [[index for index in np.array(topic).argsort()[-10:][::-1]] for topic in H]
topics_g = dict(enumerate([0]*10))
for j, topic in enumerate(topics):
    for k in xrange(j + 1, 10):
        if is_general(jaccard(topics[j], topics[k]), H_cutoff):
            topics_g[j] += 1
            topics_g[k] += 1
        else:
            topics_g[j] -= 1
            topics_g[k] -= 1

with open('/Volumes/cchen224/brand_threads/input_0615/2ksupport_user_W.data', 'r') as i:
    W = np.array(pickle.load(i))
    general = [sum(topics_g[c] * p for c, p in enumerate(t) if topics_g[c] > 0) for t in W]
    specifc = [sum(topics_g[c] * p for c, p in enumerate(t) if topics_g[c] < 0) for t in W]



def jaccard(x, y):
    x = set(x)
    y = set(y)
    return float(len(x & y)) / len(x | y)

def is_general(j_score, threshold):
    return True if j_score >= threshold else False


################################################################################################
cutoff = 0.1
ntopic = 10
counter = 0
for file in glob('/Volumes/cchen224/brand_threads/input_0615/*_brand_V.data'):
    counter += 1
    print '\n\n\n', str(counter) + '.', brand_fp

    brand_fp = re.sub('_V[.]data', '', file)

    print 'loading...',
    with open(file, 'r') as i:
        V = pickle.load(i)

    print 'modeling...',

    if V.shape[0] < ntopic or V.shape[1] < ntopic: continue
    nmf = NMF(init="nndsvd", n_components=ntopic, random_state=1, alpha=.1, l1_ratio=.8).fit(V)
    W = nmf.fit_transform(V)
    H = nmf.components_
    # len([item for item in H[0] if item != 0])

    top10 = [topic.argsort()[-ntopic:][::-1] for topic in H]

    # with open(brand_fp + '_vocab.data', 'r') as i:
    #     vocab_ = pickle.load(i)
    # top10w = [['_'.join(vocab_[index].split(' ')) for index in topic.argsort()[-10:][::-1]] for topic in H]
    # for line in top10w:
    #     for word in line:
    #         print word,
    #     print

    jd = dict()
    for j, topic in enumerate(top10):
        for k in xrange(j + 1, ntopic):
            jd[(j, k)] = jaccard(topic, top10[k])
    js = set()
    for pair in jd:
        if jd[pair] > cutoff:
            js.add(pair[0])
            js.add(pair[1])
    jc = set(range(ntopic)) - js

    print 'saving...',
    is_general = [sum([line[item] for item in js]) >= sum([line[item] for item in jc]) for line in W]
    with open(brand_fp + '_result.data', 'w') as o:
        pickle.dump(is_general, o)
    print 'done'
    # specifc = sum([W[0][item] for item in jc])
print 'ddd!'
################################################################################################

is_general = dict()
is_general_tids = dict()
for file in glob('/Volumes/cchen224/brand_threads/input_0615/*result.data'):
    with open(file, 'r') as i:
        is_general[file.split('/')[-1][:-12]] = pickle.load(i)
for file in glob('/Volumes/cchen224/brand_threads/input_0615/*tids.data'):
    with open(file, 'r') as i:
        is_general_tids[file.split('/')[-1][:-10]] = pickle.load(i)

import csv
c = 0
with open('/Volumes/cchen224/brand_threads/a.csv', 'w') as o:
    csvwriter = csv.writer(o)
    csvwriter.writerow(['brand', 'tid', 'user', 'brand_reply'])
    for key in is_general:
        user_key = re.sub('_brand', '_user', key)
        if key.endswith('_brand') and user_key in is_general:
            c += 1
            for counter, tid in enumerate(is_general_tids[key]):
                csvwriter.writerow([key[:-6], tid, is_general[user_key][counter], is_general[key][counter]])