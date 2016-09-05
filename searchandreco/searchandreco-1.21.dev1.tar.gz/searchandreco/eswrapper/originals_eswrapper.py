'''

__author__ = 'chitraangi'

The originals classes

'''

# -*- coding: utf-8 -*-

from datetime import datetime
from .originals_defines import ES_FIELD_FLAG, ES_FIELD_SH_HEADING,\
    ES_FIELD_AR_ID, ES_FIELD_AUTHOR_URL, ES_FIELD_TITLE,\
    ES_FIELD_SLUG, ES_FIELD_AUTHOR_NAME, ES_FIELD_FI_URL,\
    ES_FIELD_PUB_DATE, ES_FIELD_ID, ES_FIELD_TAGS,\
    ES_CONTENT_DOC_TYPE, ES_INDEX_MAPPING_ORIGINALS,\
    ES_INDEX_SETTINGS_ORIGINALS, ES_MLT_MIN_TERM_FREQ,\
    ES_MLT_MAX_QUERY_TERMS
from .settings import ES_CLIENT


class SearchIndexerOriginals(object):
    '''

    The indexing, updation, deletion class
    '''

    def __init__(self, index_name, doc_type=ES_CONTENT_DOC_TYPE):
        '''

        :param index_name:
        :param doc_type:
        :return:
        '''
        self.index = index_name
        self.type = doc_type

        self.esclient = ES_CLIENT

        return


    def create_index(self, mapping=ES_INDEX_MAPPING_ORIGINALS,\
                     settings=ES_INDEX_SETTINGS_ORIGINALS):
        '''

        :param index_name: name of the index which needs to be created
        :param mapping: the mapping for the ES Index

        :return: status
        '''

        result = {'status': 0, 'index_created': '', 'error': ''}

        try:

            ## In case a mapping has not
            # been provided and user wants Elastic Search to use its own mapping
            ## for each of the fields

            if self.check_index_exists() is True:
                result['status'] = 2
                result['index_created'] = self.index
                result['error'] = 'index exists'
                return result

            mapping = ES_INDEX_MAPPING_ORIGINALS

            index_parameters = {'settings': settings, 'mappings': mapping}

            # print index_parameters

            cr_status = self.esclient.indices.create(index=self.index,
                                                     body=index_parameters)

            if cr_status.has_key('acknowledged') and cr_status[
                    'acknowledged'] is True:
                result['status'] = 1
                result['index_created'] = self.index

        except Exception as (exp):
            result['status'] = 0
            result['error'] = str(exp)

            print "any exception", str(exp)

        return result

    def check_index_exists(self):
        '''

        :param index_name:
        :return:

        '''

        status = self.esclient.indices.exists(self.index)

        return status

    #### added function for indexing

    def index_single_prop_originals(self, doc_data, doc_id):
        '''

        This API adds a single document to the index

        :param index_name: name of the ES index
        :param type_name: name of the type (ie. the set of documents)
        :param id: id of the document to be indexed
        :return: status

        '''

        # print doc_data

        results = {'status': 0, 'err_message': ''}
        try:

            d_format = datetime.strptime(doc_data['pub_date'],
                                         "%B %d, %Y %H:%M:%S")
            datesortform = d_format.strftime("%Y-%m-%d")

            doc_dict = {'sh_heading': doc_data['sh_heading'],\
                        'ar_id':doc_data['ar_id'], 'title':doc_data['title'],\
                         'fImgUrl':doc_data['fImgUrl'],\
                        'tags':doc_data['tags'], 'ar_name':doc_data['ar_name'],\
                         'ar_url':doc_data['ar_url'],\
                        'pub_date':doc_data['pub_date'],\
                        'slug':doc_data['slug'], 'date_sort':datesortform,\
                        'id':doc_data['id'], 'flag':doc_data['flag']}

            self.esclient.create(index=self.index,
                                 doc_type=self.type,
                                 body=doc_dict,
                                 id=doc_id)

            results['status'] = 1

        except Exception as (exp):

            results['status'] = -1
            results['err_message'] = str(exp)

        return results

    def delete_doc_originals(self, doc_id):
        '''

        :param id: id of the document which needs to be deleted
        :return:
        '''

        results = {'status': 0, 'err_message': ''}

        if id is not None:

            try:

                self.esclient.delete(self.index, doc_type=self.type, id=doc_id)
                results['status'] = 1

            except Exception as (exp):

                results['status'] = -1
                results['err_message'] = str(exp)

        return results

    #### added function
    def update_doc_prop_originals(self, doc_id, doc_data):
        '''

        :param id: id of the document which needs to be deleted
        :return:
        '''

        results = {'status': 0, 'err_message': ''}

        if id is not None:

            try:

                d_format = datetime.strptime(doc_data['pub_date'],
                                             "%B %d, %Y %H:%M:%S")
                datesortform = d_format.strftime("%Y-%m-%d")

                doc_dict = {'sh_heading': doc_data['sh_heading'],\
                            'ar_id':doc_data['ar_id'], 'title':doc_data['title'],\
                         'fImgUrl':doc_data['fImgUrl'], 'tags':doc_data['tags'],\
                            'ar_name':doc_data['ar_name'], 'ar_url':doc_data['ar_url'],\
                            'pub_date':doc_data['pub_date'], 'slug':doc_data['slug'],\
                         'date_sort':datesortform, 'id':doc_data['id'],\
                            'flag':doc_data['flag']}


                self.esclient.update(self.index, doc_type=self.type, id=doc_id,\
                               body={"doc": doc_dict})
                results['status'] = 1

            except Exception as (exp):

                results['status'] = -1
                results['err_message'] = str(exp)

        return results


###added class
class SearchManagerOriginals(object):
    '''

    the getting search hits and mlt class
    '''

    def __init__(self, es_client, index_name, doc_type):
        '''

        :param es_client:
        :param index_name:
        :param doc_type:
        :return:
        '''
        self.esclient = es_client
        self.index = index_name
        self.type = doc_type

        return

    def more_like_this_originals(self, doc_id, stopwords=None):
        '''
        :param id: id of the document
         for which we are searching similar documents
        :return: resulting documents..
        '''


        ret_fields = [ES_FIELD_FLAG, ES_FIELD_SH_HEADING, ES_FIELD_AR_ID, ES_FIELD_TAGS,\
                       ES_FIELD_AUTHOR_URL, ES_FIELD_TITLE, ES_FIELD_SLUG,\
                       ES_FIELD_AUTHOR_NAME, ES_FIELD_FI_URL, ES_FIELD_PUB_DATE, ES_FIELD_ID]

        query_body = {"query": {
            "filtered": {"query": {
                "more_like_this": {"fields":
                                   ["title", "tags", "sh_heading", "ar_name"],
                                   "docs": [{"_id": doc_id}],
                                   "min_term_freq": ES_MLT_MIN_TERM_FREQ,
                                   "max_query_terms": ES_MLT_MAX_QUERY_TERMS,
                                   "stop_words": stopwords,
                                   "include": False},
                "filter": {"bool": {"must": {"term": {"flag": "1"}}}}
            }}
        }}


        response = self.esclient.search(index=self.index, doc_type=self.type,\
                              body=query_body, _source=ret_fields,\
                                  sort=['_score:desc', 'date_sort:desc'])

        if response['hits']['total'] == 0:

            query_body = {"filter": {"bool":
                                     {"must": {
                                         "term": {
                                             "flag": "1"
                                         }
                                     }}}}


            response = self.esclient.search(index=self.index, doc_type=self.type,\
                              body=query_body, _source=ret_fields,\
                                      sort=['_score:desc', 'date_sort:desc'])

        return response

    def search_dismax_or(self, q_str, pgno):
        '''

        :param fields_dict: This dictionary
        contains the weightages to be applied to the different fields
        :return:
        '''

        query_body = {"bool": {"should": [
            {"match": {"title": {"query": q_str,
                                 "fuzziness": 1,
                                 "operator": "and",
                                 "boost": 4}}},
            {"bool": {"should": [
                {"match": {"tags": {"query": q_str,
                                    "fuzziness": 1,
                                    "operator": "and",
                                    "boost": 3}}},
                {"bool": {"should": [
                    {"match": {"ar_name": {"query": q_str,
                                           "fuzziness": 1,
                                           "operator": "and"}}},
                    {"bool": {"should": [
                        {"match": {"sh_heading": {"query": q_str,
                                                  "fuzziness": 1,
                                                  "operator": "and"}}}
                    ]}}
                ]}}
            ]}}
        ]}}

        msize = 50
        pgno = int(pgno)


        ret_fields = [ES_FIELD_FLAG, ES_FIELD_SH_HEADING, ES_FIELD_AR_ID\
            , ES_FIELD_TAGS, ES_FIELD_AUTHOR_URL, ES_FIELD_TITLE, ES_FIELD_SLUG,\
                       ES_FIELD_AUTHOR_NAME, ES_FIELD_FI_URL, ES_FIELD_PUB_DATE,\
                       ES_FIELD_ID]

        response = self.esclient.search(self.index, doc_type=self.type,\
                                  body={"query": query_body}, _source=ret_fields,\
                                  from_=(pgno-1)*msize, size=msize,\
                                  sort=['_score:desc', 'date_sort:desc'])

        return response

    def search_dismax_or_latest(self, q_str, pgno):
        '''

        :param fields_dict: This dictionary
         contains the weightages to be applied to the different fields
        :return:
        '''

        query_body = {"bool": {"should": [
            {"match": {"title": {"query": q_str,
                                 "operator": "and",
                                 "fuzziness": 1,
                                 "boost": 4}}}, {"bool": {"should": [
                                     {"match": {"tags": {
                                         "query": q_str,
                                         "operator": "and",
                                         "fuzziness": 1,
                                         "boost": 2
                                     }}}, {"bool": {"should": [
                                         {"match": {"ar_name":
                                                    {"query": q_str,
                                                     "operator": "and",
                                                     "fuzziness": 1}}},
                                         {"match": {"sh_heading":
                                                    {"query": q_str,
                                                     "fuzziness": 1,
                                                     "operator": "and"}}}
                                     ]}}
                                 ]}}
        ]}}

        msize = 50
        pgno = int(pgno)

        ret_fields = [ES_FIELD_FLAG, ES_FIELD_SH_HEADING, ES_FIELD_AR_ID,\
                       ES_FIELD_TAGS, ES_FIELD_AUTHOR_URL, ES_FIELD_TITLE,\
                       ES_FIELD_SLUG, ES_FIELD_AUTHOR_NAME, ES_FIELD_FI_URL,\
                       ES_FIELD_PUB_DATE, ES_FIELD_ID]

        response = self.esclient.search(self.index, doc_type=self.type,\
                                  body={"query": query_body},\
                                  _source=ret_fields,\
                                  from_=(pgno-1)*msize, size=msize,\
                                  sort=['date_sort:desc'])

        return response
