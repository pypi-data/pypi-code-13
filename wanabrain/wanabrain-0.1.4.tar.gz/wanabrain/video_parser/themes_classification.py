# -*- coding: utf-8 -*-
import MySQLdb as mdb
from sklearn.svm import SVC
import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn.metrics import classification_report
import sys
import pickle
from collections import defaultdict


def themes_classification():
    con = mdb.connect('localhost', 'root', 'castor69', 'webcastor', charset='utf8', use_unicode=True)
    cur = con.cursor()

    cur.execute("SELECT caffe_features, media FROM features WHERE more_images = 1")

    caffe_features = []
    labels = []
    for triplet in cur.fetchall():

        strfeats = triplet[0]
        strfeats = strfeats.rstrip(']')
        strfeats = strfeats.lstrip('[')
        strfeats = strfeats.split()
        feats = [float(feat) for feat in strfeats]
        feats = np.array(feats)

        print(feats)
        sys.exit('')

        # print(triplet[1])
        cur.execute("SELECT themes FROM jos_inwicast_medias WHERE media_ref = %s", (triplet[1],))

        label = cur.fetchone()

        if label:
            if label[0] != '':
                labels.append(label[0])
                caffe_features.append(feats)

    cur.execute("SELECT caffe_features, media FROM features WHERE more_images is null")

    for triplet in cur.fetchall():

        strfeats = triplet[0]
        strfeats = strfeats.rstrip(']')
        strfeats = strfeats.lstrip('[')
        strfeats = strfeats.split()
        feats = [float(feat) for feat in strfeats]
        feats = np.array(feats)

        cur.execute("SELECT themes FROM jos_inwicast_medias WHERE media_ref = %s", (triplet[1],))
        label = cur.fetchone()

        # print(label)

        if label:
            label = label[0]
            if label == 'Campagne / Zone rural' or label == 'Montagne' or label == 'Ville / Zone urbaine':
                labels.append(label)
                caffe_features.append(feats)

    labels = np.array(labels)
    caffe_features = np.array(caffe_features)

    # all_labels, counts = np.unique(labels, return_counts=True)

    X_train, X_test, y_train, y_test = train_test_split(caffe_features, labels,
                                                        test_size=0.33, random_state=42)

    # clf = SVC()


    # all_labels, counts = np.unique(y_train, return_counts=True)
    # print(all_labels)
    # print(counts)

    # print('fit model')
    # clf.fit(X_train, y_train)

    clf = pickle.load(open('model.p', 'r'))

    y_test_pred = clf.predict(X_test)

    # pickle.dump(clf, open('model.p', 'w'))
    # pickle.dump(y_test_pred, open('y_test_pred.p', 'w'))
    # pickle.dump(y_test, open('y_test.p', 'w'))

    labels_not_predicted = defaultdict(int)
    for label in np.unique(y_test):
        if label not in np.unique(y_test_pred):
            labels_not_predicted[label] += 1
            ids = np.where(y_test == label)
            y_test = np.delete(y_test, ids)
            y_test_pred = np.delete(y_test_pred, ids)

    themes_classification_report = classification_report(y_test, y_test_pred)
    print(themes_classification_report)
    f = open('themes_classification_report.txt', 'w')
    f.write(themes_classification_report.encode('utf-8'))
    f.close()


themes_classification()
