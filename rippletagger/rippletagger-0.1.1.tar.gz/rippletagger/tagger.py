# -*- coding: utf-8 -*-

import os
import re

from rippletagger.models import SCRDRTree, FeatureVector

PACKAGE_PATH, _ = os.path.split(__file__)

class Tagger(SCRDRTree):
    def __init__(self, language):
        mapper = LanguageMapper()
        directory_name = mapper.directory_name(language)
        data_path = os.path.join(PACKAGE_PATH, "data", "UD_%s" % directory_name, "train.UniPOS")

        self.tree_from_file(data_path + ".RDR")
        self.word_to_tag_dict = self.dictionary_from_file(data_path + ".DICT")

    def tag(self, line):
        tagger = NaiveTagger(self.word_to_tag_dict)
        tagged_sentence_initial = tagger.tag(line)

        tagged_sentence = []

        for i, (word, tag) in enumerate(tagged_sentence_initial):
            feature = FeatureVector.build(tagged_sentence_initial, i)
            node = self.find_fired_node(feature)
            tagged_sentence.append((word, node.tag if node.depth > 0 else tag))

        return tagged_sentence

class NaiveTagger:
    def __init__(self, word_to_tag_dict):
        self.word_to_tag_dict = word_to_tag_dict

    def tag(self, line):
        words = line.strip().split()
        tagged_sentence = []
        for word in words:
            if word in [u"“", u"”", u"\""]:
                tagged_sentence.append(("''", self.word_to_tag_dict["''"]))
                continue

            tag = ''

            if word in self.word_to_tag_dict:
                tag = self.word_to_tag_dict[word]

            elif word.lower() in self.word_to_tag_dict:
                tag = self.word_to_tag_dict[word.lower()]

            else:
                if re.search(r"[0-9]+", word) is not None:
                    tag = self.word_to_tag_dict["TAG4UNKN-NUM"]

                else:
                    suffix_l2 = suffix_l3 = suffix_l4 = suffix_l5 = None
                    word_len = len(word)
                    if word_len >= 4:
                        suffix_l3 = ".*" + word[-3:]
                        suffix_l2 = ".*" + word[-2:]
                    if word_len >= 5:
                        suffix_l4 = ".*" + word[-4:]
                    if word_len >= 6:
                        suffix_l5 = ".*" + word[-5:]

                    if suffix_l5 in self.word_to_tag_dict:
                        tag = self.word_to_tag_dict[suffix_l5]
                    elif suffix_l4 in self.word_to_tag_dict:
                        tag = self.word_to_tag_dict[suffix_l4]
                    elif suffix_l3 in self.word_to_tag_dict:
                        tag = self.word_to_tag_dict[suffix_l3]
                    elif suffix_l2 in self.word_to_tag_dict:
                        tag = self.word_to_tag_dict[suffix_l2]
                    elif word[0].isupper():
                        tag = self.word_to_tag_dict["TAG4UNKN-CAPITAL"]
                    else:
                        tag = self.word_to_tag_dict["TAG4UNKN-WORD"]

            tagged_sentence.append((word, tag))

        return tagged_sentence

class LanguageMapper:
    def __init__(self):
        mapping_path = os.path.join(PACKAGE_PATH, "data", "language_mapping.txt")
        with open(mapping_path, "r") as f:
            mapping_lines = [line.strip() for line in f.readlines()]

        language_twocode = {}
        language_threecode = {}
        language_name = {}

        for line in mapping_lines:
            if line.startswith("#") or not line.strip():
                continue

            twocode, threecode, name, directory_name = line.split(", ")
            language_twocode[twocode] = directory_name.strip()
            language_threecode[threecode] = directory_name.strip()
            language_name[name] = directory_name

        self.language_twocode = language_twocode
        self.language_threecode = language_threecode
        self.language_name = language_name

    def directory_name(self, code_or_name):
        if code_or_name in self.language_twocode:
            return self.language_twocode[code_or_name]
        elif code_or_name in self.language_threecode:
            return self.language_threecode[code_or_name]
        elif code_or_name in self.language_name:
            return self.language_name[code_or_name]

        raise Exception(
            "Language '%s' not found. See models/language_mapping.txt"
            " for valid language codes" % code_or_name
        )

    def all_language_codes(self):
        return self.language_threecode.keys()
