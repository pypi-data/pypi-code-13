'''
Pagination and calls to all the search functions
'''

from .eswrapper.eswrapper import SearchManagerMultiIndex
from .eswrapper.originals_eswrapper import SearchManagerOriginals
from .eswrapper.sportscrumbs_eswrapper import SearchManagerMultiIndexSportscrumbs
from .eswrapper.settings import ES_CLIENT
from .eswrapper.defines import ES_CONTENT_DOC_TYPE
from .eswrapper.originals_defines import SWORI_INDEX_LIST
from .eswrapper.sportscrumbs_defines import ES_CONTENT_DOC_TYPE_SPRTCRMBS
from .exceptions.loggerfileload import LOGGER_SEARCH

SEARCH_MGR = SearchManagerMultiIndex(ES_CLIENT, ES_CONTENT_DOC_TYPE)

SEARCH_MGR_SPRTSCRMBS = SearchManagerMultiIndexSportscrumbs(ES_CLIENT,\
                                                            ES_CONTENT_DOC_TYPE_SPRTCRMBS)


def functiontosearch(query, pagenum, searchtype, sorttype):
    '''

    :param query:
    :param pagenum:
    :param searchtype:
    :param sorttype:
    :return:
    '''

    data = {'info': {}, 'next_page': '', 'errmsg': '', 'status': 0}

    try:
        # search function called with arguments
        if searchtype == '' and sorttype == 'score':
            data['info'] = SEARCH_MGR.search_dismax_sw(query, pagenum)

        if searchtype == '' and sorttype == 'latest':
            data['info'] = SEARCH_MGR.search_dismax_sw_latest(query, pagenum)

        if data['info']['hits']['total'] < 50:
            data['next_page'] = -1
        else:
            data['next_page'] = next_page(data['info']['hits']['hits'],
                                          pagenum)
        data['status'] = 1

    except Exception as (exp):
        data['errmsg'] = str(exp)
        data['status'] = 0
        data['info'] = {}
        LOGGER_SEARCH.error(str(exp))

    #print data
    return data


def functiontosearch_vb(query, pagenum, searchtype, sorttype):
    '''

    :param query:
    :param pagenum:
    :param searchtype:
    :param sorttype:
    :return:
    '''

    data = {'info': {}, 'next_page': '', 'errmsg': '', 'status': 0}

    try:
        # search function called with arguments
        if searchtype == '' and sorttype == 'score':
            data['info'] = SEARCH_MGR.search_dismax_vb(query, pagenum)
        elif searchtype == '' and sorttype == 'latest':
            data['info'] = SEARCH_MGR.search_dismax_vb_latest(query, pagenum)
        elif searchtype == 'article':
            data['info'] = SEARCH_MGR.search_dismax_vb_article(query, pagenum)
            # mjlist = data["info"]["suggest"]["_all"]
        elif searchtype == 'author':
            data['info'] = SEARCH_MGR.search_dismax_vb_author(query, pagenum)
            # mjlist = data["info"]["suggest"]["ar_name"]
        elif searchtype == 'category':
            data['info'] = SEARCH_MGR.search_dismax_vb_category(query, pagenum)
            # mjlist = data["info"]["suggest"]["cats"]
        else:
            data['info'] = 'No Such Searchtype exists'

        if data['info']['hits']['total'] < 50:
            data['next_page'] = -1
        else:
            data['next_page'] = next_page(data['info']['hits']['hits'],
                                          pagenum)

        data['status'] = 1

    except Exception as (exp):
        data['errmsg'] = str(exp)
        data['status'] = 0
        data['info'] = {}
        LOGGER_SEARCH.error(str(exp))

    #print data
    return data


def functiontosearch_gp(query, pagenum, searchtype, sorttype):
    '''

    :param query:
    :param pagenum:
    :param searchtype:
    :param sorttype:
    :return:
    '''

    data = {'info': {},
            'next_page': '',
            'showresultsfor': '',
            'errmsg': '',
            'status': 0}

    try:
        mjlist = []
        # search function called with arguments
        if searchtype == '' and sorttype == 'score':
            data['info'] = SEARCH_MGR.search_dismax_gp(query, pagenum)
            mjlist = data["info"]["suggest"]["_all"]

        if searchtype == '' and sorttype == 'latest':
            data['info'] = SEARCH_MGR.search_dismax_gp_latest(query, pagenum)
            mjlist = data["info"]["suggest"]["_all"]

        sug_li = []
        for sloop in mjlist:
            if sloop["options"]:
                for oloop in sloop["options"]:
                    sug_li.append(oloop["text"])

        if len(sug_li) != 0:
            data['showresultsfor'] = sug_li[0]

        for sloop in sug_li:
            if searchtype == '' and sorttype == 'score':
                data['info'] = SEARCH_MGR.search_dismax_gp(sloop, pagenum)

            if searchtype == '' and sorttype == 'latest':
                data['info'] = SEARCH_MGR.search_dismax_gp_latest(sloop,
                                                                  pagenum)

        if data['info']['hits']['total'] < 50:
            data['next_page'] = -1
        else:
            data['next_page'] = next_page(data['info']['hits']['hits'],
                                          pagenum)
        #data['next_page'] = nextPage(data['info']['hits']['hits'], pagenum)
        data['status'] = 1

    except Exception as (exp):
        data['errmsg'] = str(exp)
        data['status'] = 0
        data['info'] = {}
        LOGGER_SEARCH.error(str(exp))

    #print data
    return data


def next_page(data, pagenum):
    '''

    function to determine the next page number

    '''

    if data == []:
        next_page_val = -1
    else:
        next_page_val = int(pagenum) + 1
    return next_page_val


def findmltdocsprop(docid, prop, category):
    '''

    :param docid:
    :param prop:
    :param category:
    :return:
    '''

    data = {'info': {}, 'status': 0, 'errmsg': ''}

    try:

        data['info'] = SEARCH_MGR.more_like_this_prop(docid, prop, category)

        if data['info'] is not None:
            data['status'] = 1
        else:
            data['status'] = 0
            data['errmsg'] = 'error parameters, prop'

        return data

    except Exception as exp:

        data['errmsg'] = str(exp)
        LOGGER_SEARCH.error(str(exp))

        return data


#ORIGINALS FUNTION TO SEARCH
def functiontosearch_originals(query, pagenum, searchtype, sorttype):
    '''

    :param query:
    :param pagenum:
    :param searchtype:
    :param sorttype:
    :return:
    '''

    data = {'info': {}, 'next_page': '', 'errmsg': '', 'status': 0}

    try:

        index_name = SWORI_INDEX_LIST

        search_mgr_originals = SearchManagerOriginals(ES_CLIENT, index_name,
                                                      ES_CONTENT_DOC_TYPE)

        # search function called with arguments
        if searchtype == '' and sorttype == 'score':
            data['info'] = search_mgr_originals.search_dismax_or(query,
                                                                 pagenum)

        if searchtype == '' and sorttype == 'latest':
            data['info'] = search_mgr_originals.search_dismax_or_latest(
                query, pagenum)

        if data['info']['hits']['total'] < 50:
            data['next_page'] = -1
        else:
            data['next_page'] = next_page(data['info']['hits']['hits'],
                                          pagenum)
        data['status'] = 1

    except Exception as (exp):
        data['errmsg'] = str(exp)
        data['status'] = 0
        data['info'] = {}
        LOGGER_SEARCH.error(str(exp))

    return data


#SPORTSCRUMBS FUNCTIONS
def functiontosearch_sc(query, pagenum, sorttype):
    '''

    :param query:
    :param pagenum:
    :param sorttype:
    :return:
    '''
    data = {'info': {},
            'next_page': '',
            'errmsg': '',
            'status': 0,
            'all_hits_count': -1,
            'all_hits': {'status': 0,
                         'all_next_page': '',
                         'errmsg': ''},
            'combined_hits_count': -1,
            'combined_hits': {'status': 0},
            'aggregated_hits_count': [],
            'aggregated_hits': {'status': 0},
            'suggestions': {'status': 0,
                            'errmsg': ''}}

    try:
        # search function called with arguments
        if sorttype == 'score':
            #####combined hits
            combined_hits = SEARCH_MGR_SPRTSCRMBS.search_combined_sportcrumbs(
                query, pagenum)
            data['combined_hits'] = combined_hits
            data['combined_hits_count'] = combined_hits['hits']['total']

            #####all hits
            common_hits = SEARCH_MGR_SPRTSCRMBS.search_sportcrumbs(query,
                                                                   pagenum)

            data['all_hits'] = common_hits['hits']
            data['all_hits_count'] = common_hits['hits']['total']

            data['aggregated_hits'] = common_hits['aggregations'][
                'top-all-aggs-results']

            for avar in common_hits['aggregations']['top-all-aggs-results'][
                    'buckets']:

                aggregated_hits_count = {}

                aggregated_hits_count['key'] = avar['key']
                aggregated_hits_count['doc_count'] = avar['doc_count']

                data['aggregated_hits_count'].append(aggregated_hits_count)

            suggestions = SEARCH_MGR_SPRTSCRMBS.suggest_sportcrumbs(query,
                                                                    pagenum)
            data['suggestions'] = suggestions['suggest']
            data['suggestions']['status'] = 1

            data['info'] = SEARCH_MGR_SPRTSCRMBS.search_sportcrumbs(query,
                                                                    pagenum)

        # search function called with arguments
        if sorttype == 'latest':
            #####combined hits
            combined_hits = SEARCH_MGR_SPRTSCRMBS.search_combined_sportcrumbs(
                query, pagenum)
            data['combined_hits'] = combined_hits
            data['combined_hits_count'] = combined_hits['hits']['total']

            #####all hits
            common_hits = SEARCH_MGR_SPRTSCRMBS.search_sportcrumbs_latest(
                query, pagenum)

            data['all_hits'] = common_hits['hits']
            data['all_hits_count'] = common_hits['hits']['total']

            data['aggregated_hits'] = common_hits['aggregations'][
                'top-all-aggs-results']

            for avar in common_hits['aggregations']['top-all-aggs-results'][
                    'buckets']:

                aggregated_hits_count = {}

                aggregated_hits_count['key'] = avar['key']
                aggregated_hits_count['doc_count'] = avar['doc_count']

                data['aggregated_hits_count'].append(aggregated_hits_count)

                suggestions = SEARCH_MGR_SPRTSCRMBS.suggest_sportcrumbs(
                    query, pagenum)
                data['suggestions'] = suggestions['suggest']
                data['suggestions']['status'] = 1

                data['info'] = SEARCH_MGR_SPRTSCRMBS.search_sportcrumbs(
                    query, pagenum)

        #####all hits pagination
        if data['all_hits']['total'] < 50:
            data['all_hits']['all_next_page'] = -1
        else:
            data['all_hits']['all_next_page'] = next_page(
                data['combined_hits']['hits']['hits'], pagenum)

        data['all_hits']['status'] = 1

        data['status'] = 1

        if data['info']['hits']['total'] < 50:
            data['next_page'] = -1
        else:
            data['next_page'] = next_page(data['info']['hits']['hits'],
                                          pagenum)
        data['status'] = 1

    except Exception as (exp):
        data['errmsg'] = str(exp)
        data['all_hits']['errmsg'] = str(exp)
        data['suggestions']['status'] = 0
        data['suggestions']['errmsg'] = str(exp)
        data['status'] = 0
        data['info'] = {}
        LOGGER_SEARCH.error(str(exp))

    return data


def functiontosuggest_sc(query, pagenum, searchtype):
    '''
    :param query:
    :param pagenum:
    :param searchtype:
    :return:
    '''
    data = {'errmsg': '', 'status': 0, 'suggest': [], 'hits_total': []}

    try:
        # search function called with arguments
        if searchtype == '':
            info = SEARCH_MGR_SPRTSCRMBS.suggest_sportcrumbs(query, pagenum)
            for i in info['suggest']['title-suggestion']:
                if i['options']:
                    for optv in i['options']:
                        # print optv['text']
                        data['suggest'].append(optv['text'])
            for i in info['suggest']['team-suggestion']:
                if i['options']:
                    for optv in i['options']:
                        # print optv['text']
                        data['suggest'].append(optv['text'])
            for i in info['suggest']['player-suggestion']:
                if i['options']:
                    for optv in i['options']:
                        # print optv['text']
                        data['suggest'].append(optv['text'])
            for i in info['suggest']['action-suggestion']:
                if i['options']:
                    for optv in i['options']:
                        # print optv['text']
                        data['suggest'].append(optv['text'])
            for i in info['suggest']['sport-suggestion']:
                if i['options']:
                    for optv in i['options']:
                        # print optv['text']
                        data['suggest'].append(optv['text'])

        for dvar in data['suggest']:

            doc_dict = {}
            # print dvar
            common_hits = SEARCH_MGR_SPRTSCRMBS.search_sportcrumbs(dvar,
                                                                   pagenum)
            # print common_hits
            # print common_hits['hits']['total']
            # hits_total.append(common_hits['hits']['total'])

            doc_dict['key'] = dvar
            doc_dict['doc_count'] = common_hits['hits']['total']

            data['hits_total'].append(doc_dict)

            data['status'] = 1

    except Exception as (exp):
        data['errmsg'] = str(exp)
        data['status'] = 0
        data['info'] = {}
        LOGGER_SEARCH.error(str(exp))

    return data


def getallsuggestions(info):
    '''

    :param info:
    :return:
    '''
    suglist = []

    for i in info['suggest']['team-suggestion']:
        if i['options']:
            for optv in i['options']:
                # print optv['text']
                suglist.append(optv['text'])

    return suglist
