from .data_provider import DataProvider
from .image_processer import ImageProcesser
from .factory import ObjectFactory
from collections import defaultdict
from itertools import islice
from subprocess import call, Popen
import matplotlib.pyplot as plt
import os
import lmdb
import settings
import random
import sys
import itertools
import numpy as np
import time

sys.path.insert(0, settings.caffe_root + 'python')
import caffe as master_caffe

class NetworkTrainer():

    def __init__(self, task):

        self.task = task

    def set_db(self, working_directory, images_targets, labels, synonyms):

        if not os.path.exists(working_directory + 'database/train_rush_images'):
            os.makedirs(working_directory + 'database/train_rush_images')
        if not os.path.exists(working_directory + 'database/train_rush_labels'):
            os.makedirs(working_directory + 'database/train_rush_labels')
        if not os.path.exists(working_directory + 'database/val_rush_images'):
            os.makedirs(working_directory + 'database/val_rush_images')
        if not os.path.exists(working_directory + 'database/val_rush_labels'):
            os.makedirs(working_directory + 'database/val_rush_labels')

        map_size = 1000000 * 10 * 1000000

        train_env_images = lmdb.open(working_directory + 'database/train_rush_images', map_size=map_size)
        train_env_targets = lmdb.open(working_directory + 'database/train_rush_labels', map_size=500000000)

        val_env_images = lmdb.open(working_directory + 'database/val_rush_images', map_size=map_size)
        val_env_targets = lmdb.open(working_directory + 'database/val_rush_labels', map_size=500000000)

        train_id_img = 0
        val_id_img = 0
        train_nb_labels = defaultdict(int)
        val_nb_labels = defaultdict(int)
        all_keys = []
        with train_env_images.begin(write=True) as train_txn_images:
            with train_env_targets.begin(write=True) as train_txn_targets:
                with val_env_images.begin(write=True) as val_txn_images:
                    with val_env_targets.begin(write=True) as val_txn_targets:

                        for the_key, imgs_target in enumerate(images_targets):

                            imgs = imgs_target[0:4]
                            target = imgs_target[4]

                            keys = np.where(np.array(target) == 1)
                            all_keys = all_keys + [key for key in keys[0]]

                            id_labels = np.where(np.array(target) == 1)
                            for id_label in id_labels[0]:

                                if the_key % 6 == 0:
                                    val_nb_labels[labels[id_label]] += 4
                                else:
                                    train_nb_labels[labels[id_label]] += 4

                            im = np.array(target)  # or load whatever ndarray you need

                            if self.task == 'themes':
                                im = np.expand_dims(im, axis=0)
                            im = np.expand_dims(im, axis=0)
                            im = np.expand_dims(im, axis=0)
                            im_dat = master_caffe.io.array_to_datum(im)

                            datum = master_caffe.proto.caffe_pb2.Datum()

                            datum.channels = imgs[0].shape[2]
                            datum.height = imgs[0].shape[0]
                            datum.width = imgs[0].shape[1]
                            datum.label = 0

                            for img in imgs:

                                img = img[:, :, ::-1]
                                img = img.transpose((2, 0, 1))
                                datum.data = img.tobytes()

                                if the_key % 6 == 0:
                                    str_id = '{:08}'.format(val_id_img)
                                    val_txn_images.put(str_id.encode('ascii'), datum.SerializeToString())
                                    val_txn_targets.put(str_id.encode('ascii'), im_dat.SerializeToString())
                                    val_id_img += 1
                                else:
                                    str_id = '{:08}'.format(train_id_img)
                                    train_txn_images.put(str_id.encode('ascii'), datum.SerializeToString())
                                    train_txn_targets.put(str_id.encode('ascii'), im_dat.SerializeToString())
                                    train_id_img += 1

        train_env_images.close()
        train_env_targets.close()
        val_env_images.close()
        val_env_targets.close()

        with open(working_directory + 'database/train_stats.txt', 'a') as report:

            report.write('Total number of images in the training set : ' + str(train_id_img) + '\n')
            for label in labels:
                report.write(
                    'Number of images for the class ' + str(label) + ' : ' + str(train_nb_labels[label]) + '\n')

        with open(working_directory + 'database/val_stats.txt', 'a') as report:

            report.write('Total number of images in the validation set : ' + str(val_id_img) + '\n')
            for label in labels:
                report.write(
                    'Number of images for the class ' + str(label) + ' : ' + str(val_nb_labels[label]) + '\n')

        return np.delete(synonyms.keys(), np.unique(all_keys))

    def train_network(self, working_directory, synonyms, labels, model):

        data_provider = DataProvider('tags')
        image_processer = ImageProcesser()

        augmented_images_targets_iterable = image_processer.data_augmentation(data_provider.get_images(synonyms, labels), working_directory)

        missing_labels = self.set_db(working_directory, augmented_images_targets_iterable, labels, synonyms)

        missing_labels = np.unique(missing_labels)

        if len(missing_labels) != 0:

            with open(working_directory + '/missing_labels.txt', 'w') as file:
                file.write(
                    "Some labels are not represented in the images : " + ' - '.join(missing_labels).encode('utf-8'))
                file.write('\n \n')

                for missing_label in missing_labels:
                    file.write(missing_label.encode('utf-8') + ' : \n')
                    file.write(' - '.join(synonyms[missing_label]).encode('utf-8') + '\n \n')

            p = None

        else:

            call([settings.caffe_root + 'build/tools/compute_image_mean',
                   working_directory + 'database/train_rush_images',
                   working_directory + 'database/mean.binaryproto'])

            solver_file = working_directory + 'network/solver.prototxt'

            if not os.path.exists(working_directory + 'training'):
                os.makedirs(working_directory + 'training')

            temp_solver_name = solver_file.split('.')[0] + '_temp.prototxt'
            temp_solver = open(temp_solver_name, 'w')
            with open(solver_file, 'r') as solver:
                for line in solver:
                    if 'snapshot_prefix' in line:
                        temp_solver.write('snapshot_prefix: "' + working_directory + 'training/snapshot" \n')
                    elif './' in line:
                        temp_solver.write(line.replace('./',  working_directory + 'network/'))
                    else:
                        temp_solver.write(line)
            temp_solver.close()

            with open(working_directory + "/output.txt", "wb") as f:
                p = Popen([settings.caffe_root + "build/tools/caffe", 'train', '--solver',
                      temp_solver_name, '--weights', os.path.join(os.path.dirname(__file__), '../resources/networks/'+model+'/weights.caffemodel') ],
                     stderr=f)

        return p