from ..graph_parser.graph_browser import GraphBrowser
from key_frames import get_key_frames
from subprocess import call
from motion_detection import motion_detection
from skvideo.io import vread
import numpy as np
import logging
import subprocess
import pickle
import os
import sys
import glob
caffe_root = '/home/leo/caffe/'  # this file should be run from {caffe_root}/examples (otherwise change this line)
sys.path.insert(0, caffe_root + 'python')
import caffe
import cv2

# sys.path.remove('/home/leo/caffe/')
lisa_root = '/home/leo/lisa-caffe/'  # this file should be run from {caffe_root}/examples (otherwise change this line)
sys.path.insert(0, lisa_root + 'python')
import caffe as lisa_caffe
reload(lisa_caffe)
reload(lisa_caffe.io)
# logging.basicConfig(filename='../logs/videolib.txt',level=logging.DEBUG)
import collections
from pygraphml import GraphMLParser
import networkx as nx

def Tree():
    return collections.defaultdict(Tree)

class VideoParser():
    """
    API enabling to call video processing services  
    """

    def __init__(self, *videopaths):
        """
        Args:
            @type videopaths: Array-like of string(s)
            @param videopaths: Absolute path(s) to the video(s) to process
        """

        self.video_paths = videopaths[0]

    def initialize_transformer(self, image_mean, is_flow):

        shape = (10 * 16, 3, 227, 227)
        transformer = lisa_caffe.io.Transformer({'data': shape})
        channel_mean = np.zeros((3, 227, 227))
        for channel_index, mean_val in enumerate(image_mean):
            channel_mean[channel_index, ...] = mean_val
        transformer.set_mean('data', channel_mean)
        transformer.set_raw_scale('data', 255)
        transformer.set_channel_swap('data', (2, 1, 0))
        transformer.set_transpose('data', (2, 0, 1))
        transformer.set_is_flow('data', is_flow)
        return transformer

    def LRCN_classify_video(self, frames, net, transformer, is_flow):
        clip_length = 16
        offset = 8
        input_images = []
        for im in frames:
            input_im = lisa_caffe.io.load_image(im)
            if (input_im.shape[0] < 240):
                input_im = lisa_caffe.io.resize_image(input_im, (240, 320))
            input_images.append(input_im)
        vid_length = len(input_images)
        input_data = []
        for i in range(0, vid_length, offset):
            if (i + clip_length) < vid_length:
                input_data.extend(input_images[i:i + clip_length])
            else:  # video may not be divisible by clip_length
                input_data.extend(input_images[-clip_length:])
        output_predictions = np.zeros((len(input_data), 8))
        for i in range(0, len(input_data), clip_length):
            clip_input = input_data[i:i + clip_length]
            clip_input = lisa_caffe.io.oversample(clip_input, [227, 227])
            clip_clip_markers = np.ones((clip_input.shape[0], 1, 1, 1))
            clip_clip_markers[0:10, :, :, :] = 0
            #    if is_flow:  #need to negate the values when mirroring
            #      clip_input[5:,:,:,0] = 1 - clip_input[5:,:,:,0]
            caffe_in = np.zeros(np.array(clip_input.shape)[[0, 3, 1, 2]], dtype=np.float32)
            for ix, inputs in enumerate(clip_input):
                caffe_in[ix] = transformer.preprocess('data', inputs)
            out = net.forward_all(data=caffe_in, clip_markers=np.array(clip_clip_markers))
            output_predictions[i:i + clip_length] = np.mean(out['probs'], 1)

        print(output_predictions)

        return np.mean(output_predictions, 0).argmax(), output_predictions

    def get_movements(self):
        """
        Process video(s) to get the motion of the camera

        Return:
            @type movements: Array-like of String
            @param movements: Motion of the camera for each video
        """

        movements = {}

        for videopath in self.video_paths:

            print(videopath)

            cap = cv2.VideoCapture(videopath)
            cap = vread(videopath, backend='libav')

            try:
                movement = motion_detection(cap)
            except:
                movement = ''
                logging.exception('motion detection : ' + str(videopath))

            movements[videopath] = movement

            # net = lisa_caffe.Net(
            #     os.path.dirname(os.path.realpath(__file__)) + '/../resources/motion/deploy_lstm.prototxt',
            #     os.path.dirname(os.path.realpath(__file__)) + '/../resources/motion/weights.caffemodel',
            #     lisa_caffe.TEST)
            #
            # ucf_mean_RGB = np.zeros((3, 1, 1))
            # ucf_mean_RGB[0, :, :] = 103.939
            # ucf_mean_RGB[1, :, :] = 116.779
            # ucf_mean_RGB[2, :, :] = 128.68
            #
            # transformer_RGB = self.initialize_transformer(ucf_mean_RGB, False)
            # call([os.path.join(os.path.dirname(__file__), '../resources/motion/extract_frames.sh'), videopath, str(30)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            #
            # RGB_frames = glob.glob('RushApp/static/media/frames/'+videopath.split('/')[-1].split('.')[0]+'/*.jpg')
            #
            # class_RGB_LRCN, predictions_RGB_LRCN = self.LRCN_classify_video(RGB_frames, net, transformer_RGB, False)
            #
            # labels = pickle.load(open(os.path.join(os.path.dirname(__file__), '../resources/motion/labels.pkl'), 'r'))
            #
            # movement = labels[class_RGB_LRCN]
            #
            # movements[videopath] = movement

        return movements

    def get_landscapes(self):
        """
        Process video(s) to get the main theme (mountain / city / country ...) of the video(s)

        Return:
            @type themes: Array-like of String
            @param themes: main theme for each video
        """

        # clf = pickle.load(open(os.path.dirname(os.path.realpath(__file__))+'/resources/landscape/model.p', 'r'))
        net = caffe.Net(os.path.dirname(os.path.realpath(__file__))+'/../resources/landscapes/deploy.prototxt',
                        os.path.dirname(os.path.realpath(__file__))+'/../resources/landscapes/weights.caffemodel',
                        caffe.TEST)
        labels = pickle.load(open(os.path.dirname(os.path.realpath(__file__))+'/../resources/landscapes/labels.pkl', 'r'))
        # net, transformer = init_network('bvlc_reference_caffenet')
        print(labels)
        all_key_frames = get_key_frames(self.video_paths)

        themes = {}
        for key_frames, videopath in zip(all_key_frames, self.video_paths):
            
            potential_landscape = []
            cpt = 1
            for key_frame in key_frames:

                img = key_frame[:, :, ::-1]

                transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
                transformer.set_transpose('data', (2, 0, 1))
                transformed_image = transformer.preprocess('data', img)

                transformed_image = np.reshape(transformed_image, (1, 3, 227, 227))

                net.blobs['data'].reshape(*transformed_image.shape)
                net.blobs['data'].data[...] = transformed_image

                net.forward()

                proba = np.absolute(net.blobs['proba'].data[0, ...])
                y_pred = np.argmax(proba, 0)
                landscape = labels[y_pred]
                potential_landscape.append(landscape)

            try:
                all_landscape, landscape_counts = np.unique(potential_landscape, return_counts=True)
                themes[videopath] = all_landscape[np.argsort(landscape_counts)[::-1][0]]
            except IndexError:
                print(potential_landscape)
                themes[videopath] = ''

        return themes

    def get_tags_naive(self):

        all_key_frames = get_key_frames(self.video_paths)

        weights_files = glob.glob(os.path.join(os.path.dirname(__file__), '../resources/tags/weights/*.caffemodel'))

        # concepts_graph = nx.read_graphml(os.path.join(os.path.dirname(__file__), '../resources/onto.graphml'))

        tags = {}
        tags_probas = Tree()
        for key_frames, videopath in zip(all_key_frames, self.video_paths):

            for weights_file in weights_files:

                str_labels = weights_file.split('.')[-2].split('/')[-1]

                if 'man_work' in str_labels:
                    str_labels = str_labels.replace('man_work', 'man-work')

                threshold_probas = pickle.load(
                    open(os.path.dirname(os.path.realpath(__file__)) + '/../resources/tags/thresholds/' + str_labels + '.pkl',
                         'r'))

                dst = os.path.join(os.path.dirname(__file__), '../resources/tags/deploy')
                os.rename(dst + '/' + str_labels + '.prototxt', dst + '/old_' + str_labels + '.prototxt')
                new_deploy = open(dst + '/' + str_labels + '.prototxt', 'w')
                score_layer = False
                with open(dst + '/old_'+str_labels+'.prototxt', 'r') as deploy:
                    for line in deploy:
                        if 'name: "score"' in line:
                            score_layer = True
                        if 'num_output:' in line and score_layer is True:
                            new_deploy.write('     num_output: ' + str(len(threshold_probas)) + '\n')
                        else:
                            new_deploy.write(line)

                new_deploy.close()
                os.remove(dst + '/old_' + str_labels + '.prototxt')

                net = caffe.Net(os.path.join(os.path.dirname(__file__), '../resources/tags/deploy/' + str_labels + '.prototxt'),
                                weights_file,
                                caffe.TEST)

                probas = []
                for key_frame in key_frames:

                    img = key_frame[:, :, ::-1]

                    transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
                    transformer.set_transpose('data', (2, 0, 1))
                    transformed_image = transformer.preprocess('data', img)

                    transformed_image = np.reshape(transformed_image, (1, 3, 227, 227))

                    net.blobs['data'].reshape(*transformed_image.shape)
                    net.blobs['data'].data[...] = transformed_image

                    net.forward()

                    proba = np.absolute(net.blobs['proba'].data[0, ...])
                    probas.append(proba)

                probas = np.array(probas)
                probas = np.mean(probas, 0)

                labels = np.array(str_labels.split('_'))

                if 'nature' in str_labels:
                    estlist = probas > [0.11, 0.20, 0.5, 0.5]
                elif 'building' in str_labels:
                    estlist = probas > [0.5, 0.5, 0.51, 0.5, 0.5]
                elif 'sand' in str_labels:
                    estlist = probas > [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]

                if 1 in estlist:
                    est_classes = labels[np.where(estlist)[0]]
                else:
                    est_classes = []

                print(labels)
                print(probas)
                print('\n')

                for label, proba in zip(labels, probas):
                    tags_probas[label] = proba

                if videopath in tags.keys():
                    tags[videopath] = tags[videopath] + list(est_classes)
                else:
                    tags[videopath] = list(est_classes)

        return tags

    def get_tags(self):

        all_key_frames = get_key_frames(self.video_paths)

        graph_parser = GraphBrowser()

        str_labels = ['man_work_nature_animal_person', 'water_plant_sky_snow_cloud_rock_beach_sand_vegetation']

        tags = {}
        for key_frames, videopath in zip(all_key_frames, self.video_paths):

            labels_probas = {}
            # labels_probas[str_labels[0]] = []
            # labels_probas[str_labels[1]] = []
            for key_frame in key_frames:

                predicted_tags = graph_parser.predict(key_frame)

                for predicted_tag in predicted_tags:

                    if predicted_tag[1] is not None:

                        str_labels = '_'.join(predicted_tag[0])
                        if str_labels in labels_probas.keys():
                            labels_probas[str_labels].append((predicted_tag[0], predicted_tag[1]))
                        else:
                            labels_probas[str_labels] = []
                            labels_probas[str_labels].append((predicted_tag[0], predicted_tag[1]))

            for str_labels, all_probas in labels_probas.iteritems():

                labels = np.array(all_probas[0][0])

                probas = []
                for proba in all_probas:
                    probas.append(proba[1])

                probas = np.array(probas)
                probas = np.mean(probas, 0)

                threshold_probas = pickle.load(open(os.path.dirname(os.path.realpath(__file__)) + '/../resources/tags/'+str_labels+'/thresholds.pkl', 'r'))

                estlist = np.array(probas > threshold_probas)

                if 1 in estlist:
                    ids = np.where(estlist)[0]
                    est_classes = labels[ids]
                else:
                    est_classes = []

                if videopath in tags.keys():
                    tags[videopath] = tags[videopath] + list(est_classes)
                else:
                    tags[videopath] = list(est_classes)

        return tags

    #     classes = np.array(['person', 'animal', 'nature', 'eau', 'ouvrage'])
    #
        # net = caffe.Net(os.path.dirname(os.path.realpath(__file__))+'/resources/tags_cnn/testnet.prototxt',
        #                 os.path.dirname(os.path.realpath(__file__))+'/resources/tags_cnn/network.caffemodel',
        #                 caffe.TEST)
    #
    #     all_key_frames = get_key_frames(self.video_paths)
    #
    #
    #     tags = {}
    #     for key_frames, videopath in zip(all_key_frames, self.video_paths):
    #
    #         probas = []
    #         for key_frame in key_frames:
    #
                # img = key_frame[:,:,::-1]
                #
                # transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
                # transformer.set_transpose('data', (2,0,1))
                # transformed_image = transformer.preprocess('data', img)
                #
                # transformed_image = np.reshape(transformed_image, (1,3,227,227))
                #
                # net.blobs['data'].reshape(*transformed_image.shape)
                # net.blobs['data'].data[...] = transformed_image
                #
                # net.forward()
                #
                # proba = np.absolute(net.blobs['proba3'].data[0, ...])
                # probas.append(proba)

            # probas = np.array(probas)
            # probas = np.mean(probas, 0)
            #
            # estlist0 = (probas[0] > threshold_probas[0]).astype(int)
            # estlist1 = (probas[1] > threshold_probas[1]).astype(int)
            # estlist2 = (probas[2] > threshold_probas[2]).astype(int)
            # estlist3 = (probas[3] > threshold_probas[3]).astype(int)
            # estlist4 = (probas[4] > threshold_probas[4]).astype(int)
            #
            # estlist = np.concatenate((estlist0, estlist1, estlist2, estlist3, estlist4), 0)
            #
            # estlist = probas > threshold_probas
            #
            # if 1 in estlist:
            #     est_classes = classes[np.where(estlist)[0]]
            # else:
            #     est_classes = []
            #
            # tags[videopath] = list(est_classes)
    #
    #     return tags


        # img = cv2.imread('/home/leo/Projets/castor/images/rushs/val/PA-AUS-16-014_1.png')
     #    img = img[:,:,::-1]

     #    print(probas)
     #    # print(probas.shape)

     #     return est_classes


# vlib = Videolib(['/home/leo/Projets/castor/rushs/AS-IND-06-544_500k.f4v'])
# tags = vlib.get_tags()
# print(tags)
