'''
__author__ = 'chitraangi'

scoopwhoop originals test cases

'''
from datetime import datetime, timedelta
from .base import SearchDbTestCase
from ..eswrapper.utils import get_index_name
from ..eswrapper.settings import ES_CLIENT
from ..eswrapper.originals_defines import ES_CONTENT_DOC_TYPE
from ..eswrapper.originals_eswrapper import SearchIndexerOriginals, SearchManagerOriginals
from ..paginationspellcheck import functiontosearch_originals

## the prop value for scoopwhoop originals is or05
PROP = 'or05'


def function_to_get_docid():

    '''

    :return:
    '''
    qvar = 'best'
    pgnum = 1
    searchtype = ''
    sorttype = 'score'
    response = functiontosearch_originals(qvar, pgnum, searchtype, sorttype)

    return response['info']


class TestOriginals(SearchDbTestCase):

    '''
    scoopwhoop originals search test cases class
    '''
    #1 index article into es (all fields of data variable present)
    def test_index_article(self):

        '''

        :return:
        '''
        data_to_index = {"sh_heading":"123", "tags":["tags"],
                         "ar_url":"ar_url", "flag":1,
                         "pub_date":"June 04, 2015 13:39:33",
                         "slug":"slug", "ar_id":"12",
                         "id":"5694b6aa2d07dfc5072cb4an",
                         "title":"title", "fImgUrl":"fImgurl",
                         "ar_name":"ar_name"}
        index_name = get_index_name(PROP)
        indexer = SearchIndexerOriginals(index_name)
        response = indexer.index_single_prop_originals(data_to_index, data_to_index['id'])
        # print "scoopwhoop originals Indexed Article Response: " + str(response)
        stats = response['status']
        self.assertIsNotNone(response)
        self.assertEqual(stats, 1)


    #2 index article into es - document already exists (all fields of data variable present)
    def test_index_article_exists(self):

        '''

        :return:
        '''
        data_to_index = {"sh_heading":"123", "tags":["tags"],
                         "ar_url":"ar_url", "flag":1,
                         "pub_date":"June 04, 2015 13:39:33",
                         "slug":"slug", "ar_id":"12",
                         "id":"5694b6aa2d07dfc5072cb4an",
                         "title":"title", "fImgUrl":"fImgurl",
                         "ar_name":"ar_name"}
        index_name = get_index_name(PROP)
        indexer = SearchIndexerOriginals(index_name)
        response = indexer.index_single_prop_originals(data_to_index, data_to_index['id'])
        # print "scoopwhoop originals Indexed Article Already Exists Response: " + str(response)
        stats = response['status']
        self.assertIsNotNone(response)
        self.assertEqual(stats, -1)


    #3 index article into es - (any of the fields of data variable is not present - ex: fImgUrl)
    def test_index_art_chkdatafrmt(self):

        '''

        :return:
        '''
        data_to_index = {"sh_heading":"123", "tags":["tags"],
                         "ar_url":"ar_url", "flag":1,
                         "pub_date":"June 04, 2015 13:39:33",
                         "slug":"slug", "ar_id":"12",
                         "id":"5694b6aa2d07dfc5072cbkan",
                         "title":"title",
                         "ar_name":"ar_name"}
        index_name = get_index_name(PROP)
        indexer = SearchIndexerOriginals(index_name)
        response = indexer.index_single_prop_originals(data_to_index, data_to_index['id'])
        # print "scoopwhoop originals Indexed Article All Data Fields Not Present Response: " + str(response)
        stats = response['status']
        self.assertIsNotNone(response)
        self.assertEqual(stats, -1)


    #4 index article into es - (extra fields of data variable is present - ex: version)
    def test_ind_art_chkdatafrmt_extra(self):

        '''

        :return:
        '''
        data_to_index = {"sh_heading":"123", "tags":["tags"],
                         "ar_url":"ar_url", "flag":1,
                         "pub_date":"June 04, 2015 13:39:33",
                         "slug":"slug", "ar_id":"12", "fImgUrl":"fImgurl",
                         "id":"5694b6aa2d07dfc5072cbkan",
                         "title":"title", 'version':'1',
                         "ar_name":"ar_name"}
        index_name = get_index_name(PROP)
        indexer = SearchIndexerOriginals(index_name)
        response = indexer.index_single_prop_originals(data_to_index, data_to_index['id'])
        # print "scoopwhoop originals Indexed Article Extra Data Fields Present Response: " + str(response)
        stats = response['status']
        self.assertIsNotNone(response)
        self.assertEqual(stats, 1)


    #5 index article into es - (the datatype of fields of
    # data variable - ex: content:string, category:nested object and so on..)
    def test_art_chkfrmt_contentnotstr(self):

        '''

        :return:
        '''
        data_to_index = {"sh_heading":"123", "tags":["tags"],
                         "ar_url":"ar_url", "flag":1,
                         "pub_date":"June 04, 2015 13:39:33",
                         "slug":"slug", "ar_id":"12",
                         "id":"5694b6aa2d07dfc5072cbkan",
                         "title":[{"category_display":"category_dis",
                                     "category_slug":"category_slug"},
                                    {"category_display":"vid",
                                     "category_slug":"vid"}], 'version':'1',
                         "ar_name":"ar_name"}

        index_name = get_index_name(PROP)
        indexer = SearchIndexerOriginals(index_name)
        response = indexer.index_single_prop_originals(data_to_index, data_to_index['id'])
        # print "scoopwhoop originals Indexed Article datatype of Data Fields Response: " + str(response)
        stats = response['status']
        self.assertIsNotNone(response)
        self.assertEqual(stats, -1)


    #6 index article into es (the datatype of fields of data variable
    #  - date fields : pub_date : "June 04, 2015 13:39:33" format , datesortform)
    def test_ind_art_chkdatafrmt_date(self):

        '''

        :return:
        '''
        data_to_index = {"sh_heading":"123", "tags":["tags"],
                         "ar_url":"ar_url", "flag":1,
                         "pub_date":"Jan 04 2015 13:39:33",
                         "slug":"slug", "ar_id":"12",
                         "id":"5694b6aa2d07dfc5072cbkan",
                         "title":"title", 'version':'1',
                         "ar_name":"ar_name"}
        index_name = get_index_name(PROP)
        indexer = SearchIndexerOriginals(index_name)
        response = indexer.index_single_prop_originals(data_to_index, data_to_index['id'])
        # print "scoopwhoop originals Indexed Article Date Format Not proper Response: " + str(response)
        stats = response['status']
        self.assertIsNotNone(response)
        self.assertEqual(stats, -1)


    #7 remove article from es
    def test_remove_article(self):

        '''

        :return:
        '''
        docid = '5694b6aa2d07dfc5072cb4an'
        prop = PROP
        index_name = get_index_name(prop)
        indexer = SearchIndexerOriginals(index_name)
        response = indexer.delete_doc_originals(docid)
        # print "scoopwhoop originals Remove Article Response: " + str(response)
        stats = response['status']
        self.assertIsNotNone(response)
        self.assertEqual(stats, 1)


    #8 remove article from es - when document is not present in es
    def test_remove_article_again(self):

        '''

        :return:
        '''
        docid = '5694b6aa2d07dfc5072cb4an'
        prop = PROP
        index_name = get_index_name(prop)
        indexer = SearchIndexerOriginals(index_name)
        response = indexer.delete_doc_originals(docid)
        # print "scoopwhoop originals Remove Article Which is not in es database Response: " + str(response)
        stats = response['status']
        self.assertIsNotNone(response)
        self.assertEqual(stats, -1)


    #9 index article into es - to test edit
    def test_edit_article_1(self):

        '''

        :return:
        '''
        data_to_index = {"sh_heading":"123", "tags":["tags"],
                         "ar_url":"ar_url", "flag":1,
                         "pub_date":"June 04, 2015 13:39:33",
                         "slug":"slug", "ar_id":"12",
                         "id":"ch94b6edit07dfc5072cb4bc",
                         "title":"title", "fImgUrl":"fImgurl",
                         "ar_name":"ar_name"}
        index_name = get_index_name(PROP)
        indexer = SearchIndexerOriginals(index_name)
        response = indexer.index_single_prop_originals(data_to_index, data_to_index['id'])
        # print "scoopwhoop originals Indexed Article Response: " + str(response)
        stats = response['status']
        self.assertIsNotNone(response)
        self.assertEqual(stats, 1)


    #10 edit article info - es (proper data sent, docid exists)
    def test_edit_article_2(self):

        '''

        :return:
        '''
        docid = 'ch94b6edit07dfc5072cb4bc'
        prop = PROP
        data_to_update = {"sh_heading":"123", "tags":["tags","edit"],
                         "ar_url":"ar_url", "flag":1,
                         "pub_date":"June 04, 2015 13:39:33",
                         "slug":"slug", "ar_id":"12",
                         "id":"ch94b6edit07dfc5072cb4bc",
                         "title":"title", "fImgUrl":"fImgurl",
                         "ar_name":"ar_name"}
        index_name = get_index_name(prop)
        indexer = SearchIndexerOriginals(index_name)
        response = indexer.update_doc_prop_originals(docid, data_to_update)
        # print "scoopwhoop originals Edited Article Response: " + str(response)
        stats = response['status']
        self.assertIsNotNone(response)
        self.assertEqual(stats, 1)


    #11 edit article info - es (proper data sent, docid does not exist)
    def test_edit_article_3(self):

        '''

        :return:
        '''
        docid = '5694b6edit07idc5067cb4bc'
        prop = PROP
        data_to_update = {"sh_heading":"123", "tags":["tags"],
                         "ar_url":"ar_url", "flag":1,
                         "pub_date":"June 04, 2015 13:39:33",
                         "slug":"slug", "ar_id":"12",
                         "id":"5694b6edit07dfc5072cb4bc",
                         "title":"title", "fImgUrl":"fImgurl",
                         "ar_name":"ar_name"}
        index_name = get_index_name(prop)
        indexer = SearchIndexerOriginals(index_name)
        response = indexer.update_doc_prop_originals(docid, data_to_update)
        # print "scoopwhoop originals Edited Article docid not present Response: " + str(response)
        stats = response['status']
        self.assertIsNotNone(response)
        self.assertEqual(stats, -1)


    #12 edit article info - es (data dict - missing field sent (ex : fImgUrl), docid exists)
    def test_edit_article_4(self):

        '''

        :return:
        '''
        docid = 'ch94b6edit07dfc5072cb4bc'
        prop = PROP
        data_to_update = {"sh_heading":"123", "tags":["tags","edit"],
                         "ar_url":"ar_url", "flag":1,
                         "pub_date":"June 04, 2015 13:39:33",
                         "slug":"slug", "ar_id":"12",
                         "id":"5694b6edit07dfc5072cb4bc",
                         "title":"title",
                         "ar_name":"ar_name"}
        index_name = get_index_name(prop)
        indexer = SearchIndexerOriginals(index_name)
        response = indexer.update_doc_prop_originals(docid, data_to_update)
        # print "scoopwhoop originals Edited Article Missing field in data dict Response: " + str(response)
        stats = response['status']
        self.assertIsNotNone(response)
        self.assertEqual(stats, -1)


    #13 edit article info - es (data sent - extra field : version, docid exists)
    def test_edit_article_5(self):

        '''

        :return:
        '''
        docid = 'ch94b6edit07dfc5072cb4bc'
        prop = PROP
        data_to_update = {"sh_heading":"123", "tags":["tags"],
                         "ar_url":"ar_url", "flag":1,
                         "pub_date":"June 04, 2015 13:39:33",
                         "slug":"slug", "ar_id":"12", "fImgUrl":"fImgurl",
                         "id":"9694b6edit07dfc5072cb4bc",
                         "title":"title", 'version':'1',
                         "ar_name":"ar_name"}
        index_name = get_index_name(prop)
        indexer = SearchIndexerOriginals(index_name)
        response = indexer.update_doc_prop_originals(docid, data_to_update)
        # print "scoopwhoop originals Edited Article containing extra field Response: " + str(response)
        stats = response['status']
        self.assertIsNotNone(response)
        self.assertEqual(stats, 1)


    #14 edit article info - es (the datatype of fields
    # of data variable - ex: content:string, category:nested object, docid exists)
    def test_edit_article_6(self):

        '''

        :return:
        '''
        docid = '5694b6edit07dfc5072cb4bc'
        prop = PROP
        data_to_update = {"sh_heading":"123", "tags":["tags"],
                         "ar_url":"ar_url", "flag":1,
                         "pub_date":"June 04, 2015 13:39:33",
                         "slug":"slug", "ar_id":"12",
                         "id":"5694b6aa2d07dfc5072cbkan",
                         "title":[{"category_display":"category_dis",
                                     "category_slug":"category_slug"},
                                    {"category_display":"vid",
                                     "category_slug":"vid"}], 'version':'1',
                         "ar_name":"ar_name"}
        index_name = get_index_name(prop)
        indexer = SearchIndexerOriginals(index_name)
        response = indexer.update_doc_prop_originals(docid, data_to_update)
        # print "scoopwhoop originals Edited Article containing content
        # field as list of dict and not string Response: " + str(response)
        stats = response['status']
        self.assertIsNotNone(response)
        self.assertEqual(stats, -1)


    #15 edit article info - es
    # (data sent - date fields : pub_date : "June 04, 2015 13:39:33" format,
    # docid exists)
    def test_edit_article_7(self):

        '''

        :return:
        '''
        docid = '5694b6edit07dfc5072cb4bc'
        prop = PROP
        data_to_update = {"sh_heading":"123", "tags":["tags"],
                         "ar_url":"ar_url", "flag":1,
                         "pub_date":"Jan 04 2015 13:39:33",
                         "slug":"slug", "ar_id":"12",
                         "id":"5694b6aa2d07dfc5072cbkan",
                         "title":"title", 'version':'1',
                         "ar_name":"ar_name"}
        index_name = get_index_name(prop)
        indexer = SearchIndexerOriginals(index_name)
        response = indexer.update_doc_prop_originals(docid, data_to_update)
        # print "scoopwhoop originals Edited Article with improper date format Response: " + str(response)
        stats = response['status']
        self.assertIsNotNone(response)
        self.assertEqual(stats, -1)


    #16 search published article - es // searchtype: for future,
    # can be article,category,author... ,
    def test_search_article_1(self):

        '''

        :return:
        '''
        qvar = 'things'
        pgnum = 1
        searchtype = ''
        sorttype = 'score'
        response = functiontosearch_originals(qvar, pgnum, searchtype, sorttype)
        # print "scoopwhoop originals Search Articles Response: " + str(response)
        stats = response['status']
        self.assertIsNotNone(response)
        self.assertEqual(stats, 1)

    #17 search published article - es // searchtype: for future,
    #  can be article,category,author... , pgnum=2
    def test_search_article_2(self):

        '''

        :return:
        '''
        qvar = 'things'
        pgnum = 2
        searchtype = ''
        sorttype = 'score'
        response = functiontosearch_originals(qvar, pgnum, searchtype, sorttype)
        # print "scoopwhoop originals Search Articles Response: " + str(response)
        stats = response['status']
        self.assertIsNotNone(response)
        self.assertEqual(stats, 1)


    #18 search published article - es // searchtype: for future,
    #  can be article,category,author... , sorttype=latest
    def test_search_article_3(self):

        '''

        :return:
        '''
        qvar = 'things'
        pgnum = 1
        searchtype = ''
        sorttype = 'latest'
        response = functiontosearch_originals(qvar, pgnum, searchtype, sorttype)
        # print "scoopwhoop originals Search Articles Response: " + str(response)
        stats = response['status']
        self.assertIsNotNone(response)
        self.assertEqual(stats, 1)


    #19 search published article - es // searchtype: for future,
    #  can be article,category,author... , pgnum=2, sorttype=latest
    def test_search_article_4(self):

        '''

        :return:
        '''
        qvar = 'things'
        pgnum = 2
        searchtype = ''
        sorttype = 'latest'
        response = functiontosearch_originals(qvar, pgnum, searchtype, sorttype)
        # print "scoopwhoop originals Search Articles Response: " + str(response)
        stats = response['status']
        self.assertIsNotNone(response)
        self.assertEqual(stats, 1)


    #20 search published article - es // searchtype: for future,
    #  can be article,category,author... , pgnum=-1, sorttype=latest
    def test_search_article_5(self):

        '''

        :return:
        '''
        qvar = 'things'
        pgnum = -1
        searchtype = ''
        sorttype = 'latest'
        response = functiontosearch_originals(qvar, pgnum, searchtype, sorttype)
        # print "scoopwhoop originals Search Articles Response: " + str(response)
        stats = response['status']
        self.assertIsNotNone(response)
        self.assertEqual(stats, 0)


    #21 search published article - es // searchtype: for future,
    #  can be article,category,author... , fuzzy match
    def test_search_article_6(self):

        '''

        :return:
        '''
        qvar = 'things'
        pgnum = 1
        searchtype = ''
        sorttype = 'score'
        response = functiontosearch_originals(qvar, pgnum, searchtype, sorttype)
        # print "scoopwhoop originals Search Articles Response: " + str(response)
        stats = response['status']
        self.assertIsNotNone(response)
        self.assertEqual(stats, 1)


    #22 search published article - es // searchtype: for future,
    # can be article,category,author... ,
    # sorttype=oldest(any other except latest,score)
    def test_search_article_7(self):

        '''

        :return:
        '''
        qvar = 'things'
        pgnum = 1
        searchtype = ''
        sorttype = 'oldest'
        response = functiontosearch_originals(qvar, pgnum, searchtype, sorttype)
        # print "scoopwhoop originals Search Articles Response: " + str(response)
        stats = response['status']
        self.assertIsNotNone(response)
        self.assertEqual(stats, 0)


    #23 search published article - es // searchtype: for future,
    # can be article,category,author... , pgnum=0,
    # pgnum has to a positive integer starting from 1
    def test_search_article_8(self):

        '''

        :return:
        '''
        qvar = 'things'
        pgnum = 0
        searchtype = ''
        sorttype = 'score'
        response = functiontosearch_originals(qvar, pgnum, searchtype, sorttype)
        # print "scoopwhoop originals Search Articles Response: " + str(response)
        stats = response['status']
        self.assertIsNotNone(response)
        self.assertEqual(stats, 0)


    #24 get mlt results : docid, prop
    def test_mlt_response_1(self):

        '''

        :return:
        '''


        send_data = {'info':'', 'status':'0', 'errmsg':''}

        try :

            xvar = function_to_get_docid()
            did = xvar['hits']['hits'][0]['_source']['id']

            docid = did
            prop = PROP
            index_name = get_index_name(prop)
            indexer = SearchManagerOriginals(ES_CLIENT, index_name, ES_CONTENT_DOC_TYPE)
            send_data['info'] = indexer.more_like_this_originals(docid, prop)
            send_data['status'] = '1'
            # print "scoopwhoop originals MLT Response: " + str(send_data)

        except Exception as e :

            send_data['errmsg'] = str(e)

        self.assertIsNotNone(send_data)
        self.assertEqual(send_data['status'], '1')


    #25 get mlt results : docid, [prop : incorrect value/not given]
    def test_mlt_response_2(self):

        '''

        :return:
        '''
        send_data = {'info':'', 'status':'0', 'errmsg':''}

        try :

            xvar = function_to_get_docid()
            did = xvar['hits']['hits'][0]['_source']['id']

            docid = did
            prop = '25rt'
            index_name = get_index_name(prop)
            indexer = SearchManagerOriginals(ES_CLIENT, index_name, ES_CONTENT_DOC_TYPE)
            send_data['info'] = indexer.more_like_this_originals(docid)
            send_data['status'] = '1'
            # print "scoopwhoop originals MLT Response: " + str(send_data)

        except Exception as e :

            send_data['errmsg'] = str(e)

        self.assertIsNotNone(send_data)
        self.assertEqual(send_data['status'], '0')


    #26 get mlt results : docid, prop, the articles returned should be only flag:1
    def test_mlt_response_3(self):

        '''

        :return:
        '''

        send_data = {'info':'', 'status':'0', 'errmsg':''}

        try :

            xvar = function_to_get_docid()
            did = xvar['hits']['hits'][0]['_source']['id']

            docid = did
            prop = PROP
            index_name = get_index_name(prop)
            indexer = SearchManagerOriginals(ES_CLIENT, index_name, ES_CONTENT_DOC_TYPE)
            send_data['info'] = indexer.more_like_this_originals(docid, prop)
            send_data['status'] = '1'
            # print "scoopwhoop originals MLT Response: " + str(send_data)

            mltres = send_data['info']
            for chkfl in mltres['hits']['hits']:
                flagval = chkfl['_source']['flag']
                self.assertEqual(flagval, 1)

        except Exception as e :

            send_data['errmsg'] = str(e)

        self.assertIsNotNone(send_data)
        self.assertEqual(send_data['status'], '1')
