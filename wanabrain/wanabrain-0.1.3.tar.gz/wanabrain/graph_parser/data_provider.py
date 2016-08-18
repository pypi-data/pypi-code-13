from PIL import TarIO, Image, JpegImagePlugin
from .utils import remove_accents
from .interpreter import Interpreter
from .factory import ObjectFactory
from smb.SMBHandler import SMBHandler
import MySQLdb as mdb
import matplotlib.pyplot as plt
import tarfile
# import cv2
import glob
import numpy as np
import random
import os
import urllib2
import sys
import pickle
import fnmatch
import settings
import itertools

class DataProvider():

    def __init__(self, task):

        self.task = task

    def get_data_from_rushs(self, labels_synonyms, labels):

        interpreter = ObjectFactory.createObject(Interpreter.__name__)

        con = mdb.connect('localhost', 'root', 'castor69', 'webcastor', charset='utf8', use_unicode=True)
        cur = con.cursor()

        if self.task == 'themes':

            cur.execute('SELECT media_ref, themes FROM jos_inwicast_medias')

            refs = cur.fetchall()

            X = []
            y = []
            for ref in refs:

                media_ref = ref[0]
                label = remove_accents(ref[1].lower())

                if label != '' and label in labels_synonyms.keys():

                    medianames = glob.glob('../../images/key_frames_rushs/' + media_ref + '*.JPEG')

                    for medianame in medianames:

                        img = cv2.imread(medianame)
                        img = cv2.resize(img, (227, 227))

                        X.append(img)
                        y.append(label)

            targets, y = np.unique(y, return_inverse=True)

        elif self.task == 'tags':

            key_frames_names = glob.glob(settings.key_frames_rushs_path + '*.JPEG')
            random.shuffle(key_frames_names)

            for key_frames_name in key_frames_names:

                media_ref = key_frames_name.split('/')[-1].split('_')[0]

                cur.execute('SELECT tags FROM jos_inwicast_medias WHERE media_ref = %s', (media_ref,))

                tags = cur.fetchone()[0]
                tags = tags.split(',')
                tags = [interpreter.translate(tag.strip().lower()) for tag in tags]
                tags = [tag for tag in tags if tag is not None]

                all_tags_synonyms = []
                for tag in tags:

                    synonyms = interpreter.get_synonyms(tag)
                    all_tags_synonyms = all_tags_synonyms + synonyms

                target = []
                for label in labels:

                    label_synonyms = labels_synonyms[label]

                    label_is_hypernyms = False
                    for tag in tags:
                        if interpreter.is_hypernym(label, tag) is True:
                            label_is_hypernyms = True
                            break

                    if len(set(all_tags_synonyms).intersection(label_synonyms)) != 0 or label_is_hypernyms is True:
                        target.append(1)

                        if label == 'animal':
                            with open('/home/leo/Desktop/animal_frame.txt', 'a') as an_file:
                                an_file.write(key_frames_name)
                                print(key_frames_name)
                                img = cv2.imread(key_frames_name)
                                plt.imshow(img), plt.show()

                    else:
                        target.append(0)

                if 1 in target:

                    img = cv2.imread(key_frames_name)
                    img = cv2.resize(img, (227, 227))

                    yield(img, target)

    def get_data_from_search_engine(self, labels, search_engine=None):

        X = []
        y = []
        for root, dirnames, filenames in os.walk('../../images/bing'):

            for filename in fnmatch.filter(filenames, '*.jpg'):

                label = root.split('/')[-1]

                if label in labels.values():

                    img = cv2.imread(os.path.join(root, filename))

                    if img != None:
                        img = cv2.resize(img, (227, 227))
                        X.append(img)
                        y.append(label)

        return X,y

    def get_data_from_dataset(self, labels_synonyms, labels):

        for img, target in itertools.chain(self.get_data_from_imagenet(labels_synonyms, labels)):
            yield(img, target)

    def get_data_from_imagenet(self, labels_synonyms, labels):

        interpreter = ObjectFactory.createObject(Interpreter.__name__)

        wnid_mapping = pickle.load(open(os.path.join(os.path.dirname(__file__), '../resources/nlp/wnid_mapping.pkl'), 'r'))

        cpt = 1
        for wnid, words in wnid_mapping.iteritems():

            if cpt % 30000 == 0:
                break
                print(str(cpt) + ' synsets processed')

            for key, label in enumerate(labels):

                for word in words:

                    if interpreter.is_hypernym(label, word):

                        str_to_write = label + ' is hypernim of ' + word + ' (' + str(wnid) + ')'
                        # print(str_to_write)

                        try:
                            director = urllib2.build_opener(SMBHandler)
                            fh = director.open(
                                'smb://Production:Castor69@synology.local/projets_video/wanaclip_brain/imagenet/'+wnid+'.tar')

                            f = open('/home/leo/Desktop/'+wnid+'.tar', 'wb')
                            f.write(fh.read())
                            f.close()

                        except (urllib2.URLError,):
                            pass
                            # print(sys.exc_info()[0])
                            # print(sys.exc_info()[1])

                        if os.path.exists('/home/leo/Desktop/'+wnid+'.tar'):

                            try:
                                tar = tarfile.open(mode="r", fileobj=file('/home/leo/Desktop/'+wnid+'.tar'))

                                for img_name in tar.getnames():

                                    fp = TarIO.TarIO('/home/leo/Desktop/'+wnid+'.tar', img_name)
                                    img = Image.open(fp)

                                    if isinstance(img, JpegImagePlugin.JpegImageFile):

                                        img = cv2.resize(np.array(img), (227, 227))

                                        target = np.zeros((len(labels)))
                                        target[key] = 1

                                        yield(img, target)

                                os.remove('/home/leo/Desktop/'+wnid+'.tar')

                            except tarfile.ReadError:
                                print(sys.exc_info()[0])
                                print(sys.exc_info()[1])

            cpt += 1

    def get_images(self, labels_synonyms, labels):

        # for img, target in itertools.chain(self.get_data_from_rushs(labels_synonyms, labels),
        #                                    self.get_data_from_dataset(labels_synonyms, labels)):
        #     yield (img, target)

        for img, target in itertools.chain(self.get_data_from_rushs(labels_synonyms, labels),):
            yield (img, target)
