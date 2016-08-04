import MySQLdb as mdb
import sys
import numpy as np
import pickle
import random
from sklearn.cross_validation import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report


def get_positive_samples(cur, tag):
    cur.execute("SELECT media_ref FROM jos_inwicast_medias WHERE tags LIKE '%" + str(tag) + "%' ")

    rushs = cur.fetchall()

    pos_features = []
    for media_ref in rushs:

        media = media_ref[0]

        cur.execute("SELECT caffe_features FROM features WHERE media = %s", (media,))

        features = cur.fetchall()

        for feats in features:
            feats = feats[0]
            feats = feats.rstrip(']')
            feats = feats.lstrip('[')
            feats = feats.split()
            feats = [float(feat) for feat in feats]

            pos_features.append(feats)

    pos_features = np.array(pos_features)

    pickle.dump(pos_features, open('pos_features.p', 'w'))

    return pos_features


def get_negative_samples(cur, tag, size):
    cur.execute("SELECT media_ref FROM jos_inwicast_medias WHERE tags NOT LIKE '%" + str(tag) + "%' ")

    rushs = cur.fetchall()
    rushs = [rush[0] for rush in rushs]
    random.shuffle(rushs)

    rushs = rushs[0:size]

    neg_features = []
    for media_ref in rushs:

        media = media_ref

        cur.execute("SELECT caffe_features FROM features WHERE media = %s", (media,))

        features = cur.fetchall()

        for feats in features:
            feats = feats[0]
            feats = feats.rstrip(']')
            feats = feats.lstrip('[')
            feats = feats.split()
            feats = [float(feat) for feat in feats]

            neg_features.append(feats)

    neg_features = np.array(neg_features)

    pickle.dump(neg_features, open('neg_features.p', 'w'))

    return neg_features


def entity_recognition(tag):
    con = mdb.connect('localhost', 'leo', 'castor69', 'webcastor', charset='utf8', use_unicode=True)
    cur = con.cursor()

    # pos_features = get_positive_samples(cur, tag)
    # pos_features = pickle.load(open('pos_features.p', 'r'))
    # print(pos_features.shape)

    neg_features = get_negative_samples(cur, tag, pos_features.shape[0])
    # neg_features = pickle.load(open('neg_features.p', 'r'))
    print(neg_features.shape)

    features = np.concatenate(pos_features, neg_features)

    print(features.shape)

    pos_labels = np.empty(pos_features.shape[0])
    pos_labels.fill(1)

    neg_labels = np.empty(neg_features.shape[0])
    neg_labels.fill(0)

    labels = np.concatenate(pos_labels, neg_labels)

    print(labels.shape)

    training_data = list(zip(features, labels))
    random.shuffle(training_data)
    features, labels = zip(*training_data)

    print(features.shape)
    X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.33, random_state=42)

    clf = SVC()
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)

    pickle.dump(clf, open('model.p', 'w'))

    entity_recognition_report = classification_report(y_test, y_pred)
    f = open('entity_recognition_report.txt', 'w')
    f.write(entity_recognition_report)
    f.close()


tag = sys.argv[1]
entity_recognition(tag)
