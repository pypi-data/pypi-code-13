from sklearn.cross_validation import train_test_split
from subprocess import call
from random import shuffle
import MySQLdb as mdb
import numpy as np
import os
import glob
import cv2
import lmdb
import pickle
import sys
caffe_root = '/home/leo/caffe/'
sys.path.insert(0, caffe_root + 'python')
import caffe

def get_key_frames():

    keyframes_names = glob.glob('/home/leo/Projets/key_frames_rushs/*.JPEG') + \
                      [y for x in os.walk('/home/leo/Projets/more_images/') for y in glob.glob(os.path.join(x[0], '*.png'))]

    shuffle(keyframes_names)

    con = mdb.connect('localhost', 'root', 'castor69', 'webcastor', charset='utf8', use_unicode=True)
    cur = con.cursor()

    imgs = []
    targets = []
    for keyframes_name in keyframes_names:

        media_ref = keyframes_name.split('/')[-1].split('_')[0]

        cur.execute("SELECT themes FROM jos_inwicast_medias WHERE media_ref = %s", (media_ref,))
        theme = cur.fetchone()[0]

        if theme != '' and theme != 'Enfants' and theme != 'Evenement' and theme != 'Fand' and theme != 'Gastronomie' \
            and theme != 'Patrimoine' and theme != 'Plein_air' and theme != 'For':

            targets.append(theme)
            img = cv2.imread(keyframes_name)
            img = cv2.resize(img, (227, 227))
            imgs.append(img)

    labels, targets = np.unique(targets, return_inverse=True)

    imgs_targets = zip(imgs, targets)
    shuffle(imgs_targets)
    imgs[:], targets[:] = zip(*imgs_targets)

    return np.array(imgs), np.array(targets), labels

def set_db():

    images, targets, labels = get_key_frames()

    X_train, X_test, y_train, y_test = train_test_split(images, targets, test_size=0.2, random_state=42)

    if not os.path.exists('/home/leo/Desktop/database/'):
        os.makedirs('/home/leo/Desktop/database')
        pickle.dump(labels, open('/home/leo/Desktop/database/labels.pkl', 'w'))
        os.makedirs('/home/leo/Desktop/database/train_rushs')
        os.makedirs('/home/leo/Desktop/database/val_rushs')

    map_size = X_train[0].nbytes * 10 * len(images)

    X_train_env = lmdb.open('/home/leo/Desktop/database/train_rushs', map_size=map_size)

    with X_train_env.begin(write=True) as X_train_env_txn:

        for key, (img, target) in enumerate(zip(X_train, y_train)):

            datum = caffe.proto.caffe_pb2.Datum()
            datum.channels = img.shape[2]
            datum.height = img.shape[0]
            datum.width = img.shape[1]
            img = img[:, :, ::-1]
            img = img.transpose((2, 0, 1))
            datum.data = img.tobytes()
            datum.label = target
            str_id = '{:08}'.format(key)
            X_train_env_txn.put(str_id.encode('ascii'), datum.SerializeToString())

    map_size = X_train[0].nbytes * 10 * len(images)

    X_test_env = lmdb.open('/home/leo/Desktop/database/val_rushs', map_size=map_size)

    with X_test_env.begin(write=True) as X_test_env_txn:

        for key, (img, target) in enumerate(zip(X_test, y_test)):
            datum = caffe.proto.caffe_pb2.Datum()
            datum.channels = img.shape[2]
            datum.height = img.shape[0]
            datum.width = img.shape[1]
            img = img[:, :, ::-1]
            img = img.transpose((2, 0, 1))
            datum.data = img.tobytes()
            datum.label = target
            str_id = '{:08}'.format(key)
            X_test_env_txn.put(str_id.encode('ascii'), datum.SerializeToString())

def train_network():

    with open('/home/leo/Desktop/database/output.txt', "wb") as f:
        call([caffe_root + "build/tools/caffe", 'train', '--solver', \
              os.path.join(os.path.dirname(__file__), '../resources/landscapes/networks/deep_residual/solver.prototxt'), \
              # '--weights', os.path.join(os.path.dirname(__file__), '../resources/landscapes/networks/deep_residual/weights.caffemodel')], \
              '--snapshot', os.path.join(os.path.dirname(__file__), 'snapshot_iter_14300.solverstate')], \
             stderr=f)

if __name__ == '__main__':

    # set_db()
    train_network()