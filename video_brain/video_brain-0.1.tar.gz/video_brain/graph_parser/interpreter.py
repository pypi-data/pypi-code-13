import socket
import urllib2
from _ssl import SSLError

from gensim.models.word2vec import Word2Vec
from nltk.corpus import wordnet as wn
import numpy as np
import pickle
import os
import sys
import goslate
import time

class Interpreter:

    def __init__(self):

        model = Word2Vec.load_word2vec_format(os.path.dirname(os.path.realpath(__file__))+'/../resources/nlp/GoogleNews-vectors-negative300.bin', binary=True)
        model.init_sims(replace=True)
        self.word2vec_model = model
        self.synonyms = {}
        self.dictionary = pickle.load(open(os.path.join(os.path.dirname(__file__), '../resources/nlp/dictionary.pkl')))

    def get_synonyms(self, word):

        if word not in self.synonyms.keys():
            try:
                synonyms = self.word2vec_model.most_similar(positive=[word])
                synonyms = [similar_name[0].lower() for similar_name in synonyms]
            except KeyError:
                synonyms = []

            try:
                word_synset = wn.synset(word + '.n.01')
                for lemma in word_synset.lemmas():
                    synonyms.append(lemma.name())
            except:
                pass

            self.synonyms[word] = synonyms
        else:
            synonyms = self.synonyms[word]

        synonyms.append(word.lower())

        return list(np.unique(synonyms))

    def is_hypernym(self, label, tag):

        try:
            label_synset = wn.synset(label + '.n.01')
            tag_synset = wn.synset(tag + '.n.01')
        except:
            label_synset = None
            tag_synset = None

        if label_synset is not None and tag_synset is not None:
            tag_hypernyms = self.all_hypernyms(tag_synset)

            if len(tag_hypernyms.intersection([label_synset])) != 0:
                return True
            else:
                return False

    def semantic_similarity(self, word1, word2):
        pass

    def translate(self, word):

        if word in self.dictionary.keys():
            return self.dictionary[word].lower()
        else:

            gs = goslate.Goslate(service_urls=['https://translate.google.de'])

            try:
                tag_en = gs.translate(word, 'en')

                return tag_en

            except (socket.timeout, urllib2.HTTPError, urllib2.URLError, SSLError, TypeError):
                # print(sys.exc_info()[0])
                # print(sys.exc_info()[1])
                with open('/home/leo/Desktop/not_trad.txt', 'a') as file:
                    file.write(word.encode('utf-8') + '\n')

                return None




    def _recurse_all_hypernyms(self, synset, all_hypernyms):
        synset_hypernyms = synset.hypernyms()
        if synset_hypernyms:
            all_hypernyms += synset_hypernyms
            for hypernym in synset_hypernyms:
                self._recurse_all_hypernyms(hypernym, all_hypernyms)

    def all_hypernyms(self, synset):
        hypernyms = []
        self._recurse_all_hypernyms(synset, hypernyms)
        return set(hypernyms)


    class Factory:

        interpreter = None

        def create(self):

            if not Interpreter.Factory.interpreter:
                Interpreter.Factory.interpreter = Interpreter()

            return self.interpreter