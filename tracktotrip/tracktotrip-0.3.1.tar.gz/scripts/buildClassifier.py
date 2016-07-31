import sys
from os import listdir
from os.path import join
import numpy as np
from tracktotrip import Track
from tracktotrip.classifier import Classifier
from tracktotrip.transportation_mode import extract_features
import pickle

def process_track(filename):
    t = Track.from_gpx(filename)[0]
    t.compute_metrics()

    for segment in t.segments:
        features = extract_features(segment.points, 4)
    return features

def process_folder(folder, alias={}, skip=[]):
    files = listdir(folder)
    files = [f for f in files if f.endswith('.gpx')]

    labels = []
    features = []
    alias_keys = list(alias.keys())
    l = len(files)
    for i, gpx in enumerate(files):
        sys.stdout.write('Processing %d of %d: %s\r' % (i + 1, l, gpx))
        sys.stdout.flush()

        label = gpx.split('.')[0]
        label = label.lower()
        if label in skip:
            continue

        if label in alias_keys:
            label = alias[label]

        feature = process_track(join(folder, gpx))

        if len(feature) > 0:
            labels.append(label)
            features.append(feature)

    return features, labels

features, labels = process_folder('./dataset', alias={
    'bus': 'vehicle',
    'car': 'vehicle',
    'taxi:': 'vehicle'
}, skip=['bike'])

print('Saving features and labels')
pickle.dump(features, open('geolife.3features', 'w'))
pickle.dump(labels, open('geolife.3labels', 'w'))

print('Classifier built')
clf = Classifier()
clf.learn(features, labels)

