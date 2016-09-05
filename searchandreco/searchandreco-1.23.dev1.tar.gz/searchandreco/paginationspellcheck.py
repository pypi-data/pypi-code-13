'''
Pagination and calls to all the search functions
'''

from .eswrapper.eswrapper import SearchManagerMultiIndex
from .eswrapper.originals_eswrapper import SearchManagerOriginals
from .eswrapper.settings import ES_CLIENT
from .eswrapper.defines import ES_CONTENT_DOC_TYPE
from .eswrapper.originals_defines import SWORI_INDEX_LIST
from .exceptions.loggerfileload import logger_search

SEARCH_MGR = SearchManagerMultiIndex(ES_CLIENT, ES_CONTENT_DOC_TYPE)


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
        logger_search.error(str(exp))

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

    return data
