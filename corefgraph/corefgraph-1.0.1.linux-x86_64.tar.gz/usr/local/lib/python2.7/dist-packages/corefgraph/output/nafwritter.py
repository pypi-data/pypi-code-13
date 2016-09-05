# coding=utf-8
""" Naf format output
"""

from .basewriter import BaseDocument
from corefgraph.constants import POS, FORM, LEMMA, ID
import time
import os

__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'


class NafDocument(BaseDocument):
    """ Store the document in a KAF format(2.1).
    """
    short_name = "NAF"
    time_format = "%Y-%m-%dT%H:%M:%SZ"

    def store(self, graph, encoding, language, version, linguistic_parsers,
              start_time, end_time, hostname, **kwargs):
        """ Store the graph in a string and return it.

        @param hostname: The name of the processing machine
        @param end_time: Real processing start
        @param start_time: Real processing end
        @param graph: the graph to be stored.
        @param language: The language code inserted into the kaf file
        @param version: The version of corefgraph set on kaf
        @param encoding: Encoding set on kaf document
        @param linguistic_parsers: The linguistic parser added to kaf header.
        @param kwargs: Unused
        """
        from pynaf import NAFDocument
        if "timestamp_start" in kwargs:
            time_stamp_start = kwargs["timestamp_start"]
        else:
            time_stamp_start = time.strftime(self.time_format, start_time)

        if "timestamp_end" in kwargs:
            time_stamp_end = kwargs["timestamp_end"]
        else:
            time_stamp_end = time.strftime(self.time_format, end_time)

        if not hostname:
            hostname = os.uname()[1]

        graph_builder = graph.graph["graph_builder"]

        # Check if graph contains a pre generated kaf
        try:
            previous_kaf = graph.graph["kaf"]
        except KeyError:
            previous_kaf = None

        if previous_kaf:
            kaf_document = previous_kaf
            for lp_name, lp_version, lp_layer in linguistic_parsers:
                kaf_document.add_linguistic_processors(
                    layer=lp_layer, name=lp_name, version=lp_version,
                    begin_timestamp=time_stamp_start, end_timestamp=time_stamp_end, hostname=hostname)
            for coref_index, entity in enumerate(graph_builder.get_all_coref_entities(graph), 1):
                references = [
                    [word[ID].split("#")[0] for word in graph_builder.get_words(mention)]
                    for mention in graph_builder.get_all_entity_mentions(entity)]
                kaf_document.add_coreference("co{0}".format(coref_index), references)

        else:
            kaf_document = NAFDocument(language=language, version=version)

            words_graphs = graph_builder.get_word_graph(graph)
            for lp_name, lp_version, lp_layer in linguistic_parsers:
                kaf_document.add_linguistic_processors(
                    layer=lp_layer, name=lp_name, version=lp_version,
                    begin_timestamp=time_stamp_start, end_timestamp=time_stamp_end, hostname=hostname)

            word_index = 1
            terms_ids = dict()
            for (term_index, graph_word) in enumerate(words_graphs.vertices(), 1):
                kaf_words = graph_word[FORM].split(" ")
                words_ids = []
                for word in kaf_words:
                    word_id = "w{0}".format(word_index)
                    kaf_document.add_word(word, word_id, lemma=word[LEMMA])
                    words_ids.append(word_id)
                    word_index += 1
                term_id = "t{0}".format(term_index)
                terms_ids[graph_word] = term_id
                kaf_document.add_term(tid=term_id, pos=graph_word[POS], words=words_ids)

            for coref_index, entity in enumerate(graph_builder.get_all_coref_entities(graph), 1):
                references = [([terms_ids[word] 
                                for word in graph_builder.get_words(mention)], mention[FORM])
                              for mention in graph_builder.get_all_entity_mentions(entity)]
                kaf_document.add_coreference("co{0}".format(coref_index), references)
        kaf_document.write(self.file, encoding=encoding)
        return kaf_document
