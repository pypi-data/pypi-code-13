from .data_provider import DataProvider
from .image_processer import ImageProcesser
from .os_manager import OsManager
from .network_trainer import NetworkTrainer
from .network_evaluator import NetworkEvaluator
from .interpreter import Interpreter
from .factory import ObjectFactory
from pygraphml import GraphMLParser
from distutils.dir_util import copy_tree
from multiprocessing import Pool
import numpy as np
import pickle
import os
import sys
import shutil
import warnings
import settings
import glob
sys.path.insert(0, settings.caffe_root + 'python')
import caffe
import time

class GraphBrowser():

    def training(self, nodes, network_evaluator, user_directory, model):

        interpreter = ObjectFactory.createObject(Interpreter.__name__)
        network_trainer = NetworkTrainer('tags')
        os_manager = OsManager()

        labels = [node['name'].lower() for node in nodes]
        print(labels)

        synonyms = dict()
        for node in nodes:

            node_name = node['name'].lower()

            node_synonyms = interpreter.get_synonyms(node_name)

            for child in self.get_all_children(node):
                child_name = child['name'].lower()
                child_synonyms = interpreter.get_synonyms(child_name)

                node_synonyms = node_synonyms + child_synonyms

            synonyms[node_name] = node_synonyms

        working_directory = user_directory + '_'.join(labels) + '/'
        os_manager.create_working_directory(working_directory, model, labels)
        p = network_trainer.train_network(working_directory, synonyms, labels, model)
        if p is not None:
            network_evaluator.add_training((p, working_directory, labels))

    def inference(self, nodes, image):

        # if 'nature' in [node['name'].lower() for node in nodes]:
        #     nodes.reverse()
        labels = [node['name'].lower() for node in nodes]

        weight_file = os.path.join(os.path.dirname(__file__), '../resources/tags/'+'_'.join(labels)+'/weights.caffemodel')

        net = caffe.Net(os.path.join(os.path.dirname(__file__), '../resources/tags/'+'_'.join(labels)+'/deploy.prototxt'),
                        weight_file,
                        caffe.TEST)
        # threshold_probas = pickle.load(
        #     open(os.path.dirname(os.path.realpath(__file__)) + '/../resources/tags/' + '_'.join(labels) + '/thresholds.pkl',
        #          'r'))

        img = image[:, :, ::-1]

        transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
        transformer.set_transpose('data', (2, 0, 1))
        transformed_image = transformer.preprocess('data', img)

        transformed_image = np.reshape(transformed_image, (1, 3, 227, 227))

        net.blobs['data'].reshape(*transformed_image.shape)
        net.blobs['data'].data[...] = transformed_image

        net.forward()

        probas = np.absolute(net.blobs['proba'].data[0, ...])

        return probas

    def get_all_children(self, node):

        children = [node]
        if len(node.children()) != 0:
            for child in node.children():
                children = children + self.get_all_children(child)
        else:
            return children

        return children

    def browse_graph(self, nodes, network_evaluator, user_directory, phase, model, image=None, probas_labels=None):

        node_names = [node['name'].lower() for node in nodes]

        if phase == 'fit' and 'nature' in node_names:
        # if phase == 'fit' and 'building' in node_names:
        # if phase == 'fit' and 'sand' in node_names:
        # if phase == 'fit':
            self.training(nodes, network_evaluator, user_directory, model)
        # elif phase == 'predict' and ('beach' in node_names or 'nature' in node_names):
        elif phase == 'predict':
            probas = self.inference(nodes, image)
            probas_labels.append((node_names, probas))

        for key, node in enumerate(nodes):

                childs = node.children()

                if len(childs) != 0:
                    proba_labels = self.browse_graph(childs, network_evaluator, user_directory, phase, model, image, probas_labels)
                    probas_labels.append(proba_labels)
                else:
                    if 'nature' in node_names:
                        return (node_names, probas)
                    else:
                        return (node_names, None)

        return proba_labels

    def fit(self, user_directory, model='deep_residual'):

        parser = GraphMLParser()
        graph = parser.parse(os.path.join(os.path.dirname(__file__), '../resources/onto.graphml'))

        network_evaluator = NetworkEvaluator()
        network_evaluator.monitor()

        for node in graph.nodes():
            if node['name'] == 'Entity':
                root = node

        self.browse_graph(root.children(), network_evaluator, user_directory, 'fit', model, None, [])

    def predict(self, image):

        parser = GraphMLParser()
        graph = parser.parse(os.path.join(os.path.dirname(__file__), '../resources/onto.graphml'))

        for node in graph.nodes():
            if node['name'] == 'Entity':
                root = node

        probas_labels = []
        self.browse_graph(root.children(), None, None, 'predict', None, image, probas_labels)

        return probas_labels