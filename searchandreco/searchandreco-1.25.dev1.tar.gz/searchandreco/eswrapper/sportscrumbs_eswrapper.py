'''
__author__ = 'chitraangi'

the sportscrumbs eswrapper functions

'''

import json
from datetime import datetime
from elasticsearch import helpers
from .sportscrumbs_defines import ES_CONTENT_DOC_TYPE_SPRTCRMBS, ES_INDEX_MAPPING,\
    ES_INDEX_SETTINGS, MAPPING_TYPE, USE_NO_MAPPING, ES_FIELD_ID,\
    ES_FIELD_SH_HEADING, ES_FIELD_CONTENT, ES_FIELD_AR_ID,\
    ES_FIELD_TAGS, ES_FIELD_TITLE, ES_FIELD_SLUG, ES_FIELD_AUTHOR_NAME,\
    ES_FIELD_DIS_NAME, ES_FIELD_FI_URL, ES_FIELD_PUB_DATE, SC_INDEX_LIST
from .settings import ES_CLIENT


class SearchIndexerSportscrumbs(object):
    '''
    sportscrumbs indexer class
    '''

    def __init__(self, index_name, doc_type=ES_CONTENT_DOC_TYPE_SPRTCRMBS):
        '''

        :param index_name:
        :param doc_type:
        :return:
        '''
        self.index = index_name
        self.type = doc_type

        self.esclient = ES_CLIENT

        return

    def create_index(self,
                     mapping=ES_INDEX_MAPPING,
                     settings=ES_INDEX_SETTINGS):
        '''
        :param index_name: name of the index which needs to be created
        :param mapping: the mapping for the ES Index
        :return: status
        '''

        result = {'status': 0, 'index_created': '', 'error': ''}

        try:

            ## In case a mapping has not been
            # provided and user wants Elastic Search to use its own mapping
            ## for each of the fields

            if self.check_index_exists() is True:
                result['status'] = 2
                result['index_created'] = self.index
                result['error'] = 'index exists'
                return result

            if MAPPING_TYPE == USE_NO_MAPPING:
                cr_status = self.esclient.indices.create(index=self.index)
            else:
                ## in case by mistake mapping comes to be None here, we still define our mapping..

                if mapping is None:
                    mapping = ES_INDEX_MAPPING

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

        return result

    def check_index_exists(self):
        '''
        :param index_name:
        :return:
        '''
        status = self.esclient.indices.exists(self.index)
        return status

    #### added function for indexing
    def index_single_prop_sprtcrmbs(self, doc_data, doc_id):
        '''
        This API adds a single document to the index
        :param index_name: name of the ES index
        :param type_name: name of the type (ie. the set of documents)
        :param id: id of the document to be indexed
        :return: status
        '''

        results = {'status': 0, 'err_message': ''}
        try:

            dfrmt = datetime.strptime(doc_data['pub_date'],
                                      "%B %d, %Y %H:%M:%S")
            datesortform = dfrmt.strftime("%Y-%m-%d")

            input_list_title = [doc_data['title']]

            # print doc_data['tags']

            dteam = doc_data['tags'][0]
            dsport = doc_data['tags'][1]
            daction = doc_data['tags'][2]
            dplayer = doc_data['tags'][3]

            doc_dict = {'sh_heading': doc_data['sh_heading'], 'pub_date':doc_data['pub_date'],\
                        'slug':doc_data['slug'], 'date_sort':datesortform, \
                        'ar_id':doc_data['ar_id'], 'title':doc_data['title'],\
                        'fImgUrl':doc_data['fImgUrl'], 'tags':doc_data['tags'],\
                        'id':doc_data['id'], 'content':doc_data['content'],\
                        'ar_name':doc_data['ar_name'], 'team': dteam,\
                        'sport': dsport, 'action': daction, 'player':dplayer,\
                        'title-suggest':{
                            "input" : input_list_title,##list of all the inputs
                            "payload" : ##json data of document to be returned
                            {
                                "sh_heading": doc_data["sh_heading"],
                                "pub_date":doc_data["pub_date"],
                                "slug" : doc_data["slug"],
                                "ar_id" : doc_data["ar_id"],
                                "title" : doc_data["title"],
                                "fImgUrl":doc_data["fImgUrl"],
                                "tags":doc_data["tags"],
                                "id" : doc_data["id"],
                                "content":doc_data["content"],
                                "ar_name":doc_data["ar_name"]
                            }
                        },
                        'team-suggest':{
                            #"input" : flist[ti+1:si],##list of all the inputs
                            "input" : dteam,##list of all the inputs
                            "payload" : ##json data of document to be returned
                            {
                                "sh_heading": doc_data["sh_heading"],
                                "pub_date":doc_data["pub_date"],
                                "slug" : doc_data["slug"],
                                "ar_id" : doc_data["ar_id"],
                                "title" : doc_data["title"],
                                "fImgUrl":doc_data["fImgUrl"],
                                "tags":doc_data["tags"],
                                "id" : doc_data["id"],
                                "content":doc_data["content"],
                                "ar_name":doc_data["ar_name"]
                            }
                            },
                        'sport-suggest':
                            {
                                # "input" : flist[si+1:ai],##list of all the inputs
                                "input" : dsport,##list of all the inputs
                                "payload" : ##json data of document to be returned
                                {
                                    "sh_heading": doc_data["sh_heading"],
                                    "pub_date":doc_data["pub_date"],
                                    "slug" : doc_data["slug"],
                                    "ar_id" : doc_data["ar_id"],
                                    "title" : doc_data["title"],
                                    "fImgUrl":doc_data["fImgUrl"],
                                    "tags":doc_data["tags"],
                                    "id" : doc_data["id"],
                                    "content":doc_data["content"],
                                    "ar_name":doc_data["ar_name"]
                                }
                            },
                        'action-suggest':
                            {
                                #"input" : flist[ai+1:pi],##list of all the inputs
                                "input" : daction,##list of all the inputs
                                "payload" : ##json data of document to be returned
                                {
                                    "sh_heading": doc_data["sh_heading"],
                                    "pub_date":doc_data["pub_date"],
                                    "slug" : doc_data["slug"],
                                    "ar_id" : doc_data["ar_id"],
                                    "title" : doc_data["title"],
                                    "fImgUrl":doc_data["fImgUrl"],
                                    "tags":doc_data["tags"],
                                    "id" : doc_data["id"],
                                    "content":doc_data["content"],
                                    "ar_name":doc_data["ar_name"]
                                }
                            },
                        'player-suggest':
                            {
                                #"input" : flist[pi+1:],##list of all the inputs
                                "input" : dplayer,##list of all the inputs
                                "payload" : ##json data of document to be returned
                                {
                                    "sh_heading": doc_data["sh_heading"],
                                    "pub_date":doc_data["pub_date"],
                                    "slug" : doc_data["slug"],
                                    "ar_id" : doc_data["ar_id"],
                                    "title" : doc_data["title"],
                                    "fImgUrl":doc_data["fImgUrl"],
                                    "tags":doc_data["tags"],
                                    "id" : doc_data["id"],
                                    "content":doc_data["content"],
                                    "ar_name":doc_data["ar_name"]
                                }
                            }
                       }

            self.esclient.create(index=self.index,
                                 doc_type=self.type,
                                 body=doc_dict,
                                 id=doc_id)

            results['status'] = 1
            print doc_dict

        except Exception as (exp):

            results['status'] = -1
            results['err_message'] = str(exp)

        return results

    def index_bulk(self, docs, total):
        '''
        Will be using the bulk insert api of Elasticsearch here and see what happens
        :param json_data:
        :return:
        '''

        actions = []

        if total == 0 or len(docs) == 0:
            return

        ## iterate through the list of docs
        for entry in docs:

            doc_id = entry[ES_FIELD_ID]

            if doc_id is None:
                continue

            action = {
                "_index": self.index,
                "_type": self.type,
                "_id": doc_id,
                "_source": json.dumps(entry)
            }

            actions.append(action)

        helpers.bulk(self.esclient, actions)

        return

    def delete_doc_sprtcrmbs(self, doc_id):
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
    def update_doc_prop_sprtcrmbs(self, doc_id, doc_data):
        '''
        :param id: id of the document which needs to be deleted
        :return:
        '''

        results = {'status': 0, 'err_message': ''}

        if id is not None:

            try:

                dfrmt = datetime.strptime(doc_data['pub_date'],
                                          "%B %d, %Y %H:%M:%S")
                datesortform = dfrmt.strftime("%Y-%m-%d")

                doc_dict = {'sh_heading': doc_data['sh_heading'],\
                            'ar_id':doc_data['ar_id'], 'title':doc_data['title'],\
                            'fImgUrl':doc_data['fImgUrl'], 'tags':doc_data['tags'],\
                            'content':doc_data['content'], 'ar_name':doc_data['ar_name'],\
                            'swcats':doc_data['swcats'], 'ar_url':doc_data['ar_url'],\
                            'pub_date':doc_data['pub_date'], 'slug':doc_data['slug'],\
                            'date_sort':datesortform}

                self.esclient.update(self.index, doc_type=self.type,\
                                     id=doc_id, body={"doc": doc_dict})
                results['status'] = 1

            except Exception as (exp):
                results['status'] = -1
                results['err_message'] = str(exp)

        return results


###added class
class SearchManagerMultiIndexSportscrumbs(object):
    '''
    Search class for Sportscrumbs
    '''

    def __init__(self, es_client, doc_type):
        '''

        :param es_client:
        :param doc_type:
        :return:
        '''
        self.type = doc_type
        self.esclient = es_client

        return

    def search_sportcrumbs(self, q_str, pgno):
        '''
        :param fields_dict: This dictionary
        contains the weightages to be applied to the different fields
        :return:
        '''

        # print q_str
        q_str_aggs = q_str.replace(',', '|')
        # print q_str_aggs
        query_body = {"query": {"match":
                                {"tags": {"query": q_str,
                                          "fuzziness": 1,
                                          "operator": "or"}}},
                      "size": 50,
                      "aggs": {
                          "top-all-aggs-results": {
                              "terms": {
                                  "field": "tags",
                                  "include": q_str_aggs,
                                  "size": 10
                              },
                              "aggs": {
                                  "top-aggs-results": {
                                      "top_hits": {
                                          "size": 20
                                      }
                                  }
                              }
                          }
                      }}

        msize = 50
        pgno = int(pgno)

        index_list = SC_INDEX_LIST

        ret_fields = [ES_FIELD_SH_HEADING, ES_FIELD_CONTENT, ES_FIELD_AR_ID,\
                       ES_FIELD_TAGS, ES_FIELD_TITLE, ES_FIELD_SLUG, ES_FIELD_AUTHOR_NAME,\
                       ES_FIELD_DIS_NAME, ES_FIELD_FI_URL, ES_FIELD_PUB_DATE, ES_FIELD_ID]

        response = self.esclient.search(index=index_list, doc_type=self.type, body=query_body,\
                                        _source=ret_fields, from_=(pgno-1)*msize, size=msize,\
                                        sort=['_score:desc', 'date_sort:desc'])

        return response

    def search_sportcrumbs_latest(self, q_str, pgno):
        '''
        :param fields_dict: This dictionary contains
         the weightages to be applied to the different fields
        :return:
        '''

        # print q_str
        q_str_aggs = q_str.replace(',', '|')
        # print q_str_aggs
        query_body = {"query": {"match": {"tags":
                                          {"query": q_str,
                                           "fuzziness": 1,
                                           "operator": "or"}}},
                      "size": 50,
                      "aggs": {
                          "top-all-aggs-results": {
                              "terms": {
                                  "field": "tags",
                                  "include": q_str_aggs,
                                  "size": 10
                              },
                              "aggs": {"top-aggs-results": {
                                  "top_hits": {
                                      "size": 20
                                  }
                              }}
                          }
                      }}

        msize = 50
        pgno = int(pgno)

        index_list = SC_INDEX_LIST

        ret_fields = [ES_FIELD_SH_HEADING, ES_FIELD_CONTENT, ES_FIELD_AR_ID,\
                       ES_FIELD_TAGS, ES_FIELD_TITLE, ES_FIELD_SLUG, ES_FIELD_AUTHOR_NAME,\
                       ES_FIELD_DIS_NAME, ES_FIELD_FI_URL, ES_FIELD_PUB_DATE, ES_FIELD_ID]

        response = self.esclient.search(index=index_list, doc_type=self.type, body=query_body,\
                                        _source=ret_fields, from_=(pgno-1)*msize,\
                                        size=msize, sort=['date_sort:desc', '_score:desc'])

        return response

    def search_combined_sportcrumbs(self, q_str, pgno):
        '''
        :param fields_dict: This dictionary contains
         the weightages to be applied to the different fields
        :return:
        '''

        # print q_str
        # q_str_aggs = q_str.replace(',', '|')
        # print q_str_aggs
        query_body = {"query": {"match": {"tags":
                                          {"query": q_str,
                                           "fuzziness": 1,
                                           "operator": "and"}}}}

        msize = 50

        pgno = int(pgno)

        index_list = SC_INDEX_LIST

        ret_fields = [ES_FIELD_SH_HEADING, ES_FIELD_CONTENT, ES_FIELD_AR_ID,\
                       ES_FIELD_TAGS, ES_FIELD_TITLE, ES_FIELD_SLUG, ES_FIELD_AUTHOR_NAME,\
                       ES_FIELD_DIS_NAME, ES_FIELD_FI_URL, ES_FIELD_PUB_DATE, ES_FIELD_ID]

        response = self.esclient.search(index=index_list, doc_type=self.type, body=query_body,\
                                        _source=ret_fields, from_=(pgno-1)*msize,\
                                        size=msize, sort=['_score:desc', 'date_sort:desc'])

        return response

    def suggest_sportcrumbs(self, q_str, pgno):
        '''
        :param fields_dict: This dictionary contains
         the weightages to be applied to the different fields
        :return:
        '''

        # print q_str
        # q_str_aggs = q_str.replace(',', '|')
        # print q_str_aggs

        query_body = {"suggest": {
            "team-suggestion": {
                "text": q_str,
                "completion": {
                    "field": "team-suggest",
                    "size": 30
                }
            },
            "title-suggestion": {
                "text": q_str,
                "completion": {
                    "field": "title-suggest",
                    "size": 30
                }
            },
            "player-suggestion": {
                "text": q_str,
                "completion": {
                    "field": "player-suggest",
                    "size": 30
                }
            },
            "sport-suggestion": {
                "text": q_str,
                "completion": {
                    "field": "sport-suggest",
                    "size": 30
                }
            },
            "action-suggestion": {
                "text": q_str,
                "completion": {
                    "field": "action-suggest",
                    "size": 30
                }
            }
        },
                      "query": {"match": {
                          "tags": {
                              "query": q_str,
                              "fuzziness": 1,
                              "operator": "or"
                          }
                      }}}

        msize = 50
        pgno = int(pgno)

        index_list = SC_INDEX_LIST

        ret_fields = [ES_FIELD_SH_HEADING, ES_FIELD_CONTENT, ES_FIELD_AR_ID,\
                       ES_FIELD_TAGS, ES_FIELD_TITLE, ES_FIELD_SLUG, ES_FIELD_AUTHOR_NAME,\
                       ES_FIELD_DIS_NAME, ES_FIELD_FI_URL, ES_FIELD_PUB_DATE, ES_FIELD_ID]

        response = self.esclient.search(index=index_list, doc_type=self.type, body=query_body,\
                                        _source=ret_fields, from_=(pgno-1)*msize,\
                                        size=0, sort=['_score:desc', 'date_sort:desc'])

        return response
