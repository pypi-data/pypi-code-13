'''
__author__ = 'chitraangi'

scoopwhoop test cases

'''
from datetime import datetime, timedelta
from .base import SearchDbTestCase
from ..eswrapper.utils import get_index_name
from ..eswrapper.eswrapper import SearchIndexer
from ..paginationspellcheck import functiontosearch, findmltdocsprop

## the prop value for scoopwhoop is 25rt
PROP = '25rt'


def function_to_get_id_cat_mlt():

    '''

    :return:
    '''
    qvar = 'scoopwhoop'
    pgnum = 1
    searchtype = ''
    sorttype = 'score'
    response = functiontosearch(qvar, pgnum, searchtype, sorttype)

    return response['info']


class TestScoopwhoop(SearchDbTestCase):

    '''
    Scoopwhoop search test cases class
    '''
    #1 index article into es (all fields of data variable present)
    def test_index_article(self):

        '''

        :return:
        '''
        data_to_index = {"id":"5694b6aa2d07dfc5072cb4bc", "slug":"slug",
                         "ar_url":"ar_url", "ar_name":"ar_name", "content":"content",
                         "tags":["tags"], "fImgUrl":"fImgurl", "title":"title",
                         "ar_id":"12", "sh_heading":"123",
                         "pub_date":"June 04, 2015 13:39:33",
                         "swcats":[{"category_display":"category_dis",
                                    "category_slug":"category_slug"},
                                   {"category_display":"vid",
                                    "category_slug":"vid"}]}
        index_name = get_index_name(PROP)
        indexer = SearchIndexer(index_name)
        response = indexer.index_single_prop(data_to_index, data_to_index['id'])
        # print "Scoopwhoop Indexed Article Response: " + str(response)
        stats = response['status']
        self.assertIsNotNone(response)
        self.assertEqual(stats, 1)


    #2 index article into es - document already exists (all fields of data variable present)
    def test_index_article_exists(self):

        '''

        :return:
        '''
        data_to_index = {"id":"5694b6aa2d07dfc5072cb4bc", "slug":"slug",
                         "ar_url":"ar_url", "ar_name":"ar_name", "content":"content",
                         "tags":["tags"], "fImgUrl":"fImgurl", "title":"title",
                         "ar_id":"12", "sh_heading":"123",
                         "pub_date":"June 04, 2015 13:39:33",
                         "swcats":[{"category_display":"category_dis",
                                    "category_slug":"category_slug"},
                                   {"category_display":"vid",
                                    "category_slug":"vid"}]}
        index_name = get_index_name(PROP)
        indexer = SearchIndexer(index_name)
        response = indexer.index_single_prop(data_to_index, data_to_index['id'])
        # print "Scoopwhoop Indexed Article Already Exists Response: " + str(response)
        stats = response['status']
        self.assertIsNotNone(response)
        self.assertEqual(stats, -1)


    #3 index article into es - (any of the fields of data variable is not present - ex: fImgUrl)
    def test_index_art_chkdatafrmt(self):

        '''

        :return:
        '''
        data_to_index = {"id":"7694b6aa2d07dfc5072cb4bc", "slug":"slug",
                         "ar_url":"ar_url", "ar_name":"ar_name",
                         "content":"content", "tags":["tags"],
                         "title":"title", "ar_id":"12", "sh_heading":"123",
                         "pub_date":"June 04, 2015 13:39:33",
                         "swcats":[{"category_display":"category_dis",
                                    "category_slug":"category_slug"},
                                   {"category_display":"vid",
                                    "category_slug":"vid"}]}
        index_name = get_index_name(PROP)
        indexer = SearchIndexer(index_name)
        response = indexer.index_single_prop(data_to_index, data_to_index['id'])
        # print "Scoopwhoop Indexed Article All Data Fields Not Present Response: " + str(response)
        stats = response['status']
        self.assertIsNotNone(response)
        self.assertEqual(stats, -1)


    #4 index article into es - (extra fields of data variable is present - ex: version)
    def test_ind_art_chkdatafrmt_extra(self):

        '''

        :return:
        '''
        data_to_index = {"id":"7694b6aa2d07dfc5072cb4bc", "slug":"slug",
                         "ar_url":"ar_url", "version":"version", "ar_name":"ar_name",
                         "content":"content", "tags":["tags"], "fImgUrl":"fImgurl",
                         "title":"title", "ar_id":"12", "sh_heading":"123",
                         "pub_date":"June 04, 2015 13:39:33",
                         "swcats":[{"category_display":"category_dis",
                                    "category_slug":"category_slug"},
                                   {"category_display":"vid",
                                    "category_slug":"vid"}]}
        index_name = get_index_name(PROP)
        indexer = SearchIndexer(index_name)
        response = indexer.index_single_prop(data_to_index, data_to_index['id'])
        # print "Scoopwhoop Indexed Article Extra Data Fields Present Response: " + str(response)
        stats = response['status']
        self.assertIsNotNone(response)
        self.assertEqual(stats, 1)


    #5 index article into es - (the datatype of fields of
    # data variable - ex: content:string, category:nested object and so on..)
    def test_art_chkfrmt_contentnotstr(self):

        '''

        :return:
        '''
        data_to_index = {"id":"d694b6aa2d07dfc5072cb4bc",
                         "slug":"slug", "ar_url":"ar_url", "ar_name":"ar_name",
                         "content":[{"category_display":"category_dis",
                                     "category_slug":"category_slug"},
                                    {"category_display":"vid",
                                     "category_slug":"vid"}], "tags":["tags"],
                         "fImgUrl":"fImgurl", "title":"title", "ar_id":"12",
                         "sh_heading":"123", "pub_date":"June 04, 2015 13:39:33",
                         "swcats":[{"category_display":"category_dis",
                                    "category_slug":"category_slug"},
                                   {"category_display":"vid",
                                    "category_slug":"vid"}]}
        index_name = get_index_name(PROP)
        indexer = SearchIndexer(index_name)
        response = indexer.index_single_prop(data_to_index, data_to_index['id'])
        # print "Scoopwhoop Indexed Article datatype of Data Fields Response: " + str(response)
        stats = response['status']
        self.assertIsNotNone(response)
        self.assertEqual(stats, -1)


    #6 index article into es (the datatype of fields of data variable
    #  - date fields : pub_date : "June 04, 2015 13:39:33" format , datesortform)
    def test_ind_art_chkdatafrmt_date(self):

        '''

        :return:
        '''
        data_to_index = {"id":"dateb6aa2d07dfc5072cb4bc", "slug":"slug",
                         "ar_url":"ar_url", "ar_name":"ar_name", "content":"content",
                         "tags":["tags"], "fImgUrl":"fImgurl", "title":"title",
                         "ar_id":"12", "sh_heading":"123",
                         "pub_date":"Jan 04 2015 13:39:33",
                         "swcats":[{"category_display":"category_dis",
                                    "category_slug":"category_slug"},
                                   {"category_display":"vid",
                                    "category_slug":"vid"}]}
        index_name = get_index_name(PROP)
        indexer = SearchIndexer(index_name)
        response = indexer.index_single_prop(data_to_index, data_to_index['id'])
        # print "Scoopwhoop Indexed Article Date Format Not proper Response: " + str(response)
        stats = response['status']
        self.assertIsNotNone(response)
        self.assertEqual(stats, -1)


    #7 remove article from es
    def test_remove_article(self):

        '''

        :return:
        '''
        docid = '5694b6aa2d07dfc5072cb4bc'
        prop = PROP
        index_name = get_index_name(prop)
        indexer = SearchIndexer(index_name)
        response = indexer.delete_doc(docid)
        # print "Scoopwhoop Remove Article Response: " + str(response)
        stats = response['status']
        self.assertIsNotNone(response)
        self.assertEqual(stats, 1)


    #8 remove article from es - when document is not present in es
    def test_remove_article_again(self):

        '''

        :return:
        '''
        docid = '5694b6aa2d07dfc5072cb4bc'
        prop = PROP
        index_name = get_index_name(prop)
        indexer = SearchIndexer(index_name)
        response = indexer.delete_doc(docid)
        # print "Scoopwhoop Remove Article Which is not in es database Response: " + str(response)
        stats = response['status']
        self.assertIsNotNone(response)
        self.assertEqual(stats, -1)


    #9 index article into es - to test edit
    def test_edit_article_1(self):

        '''

        :return:
        '''
        data_to_index = {"id":"5694b6edit07dfc5072cb4bc", "slug":"slug",
                         "ar_url":"ar_url", "ar_name":"ar_name",
                         "content":"content", "tags":["tags"],
                         "fImgUrl":"fImgurl", "title":"title",
                         "ar_id":"12", "sh_heading":"123",
                         "pub_date":"June 04, 2015 13:39:33",
                         "swcats":[{"category_display":"category_dis",
                                    "category_slug":"category_slug"},
                                   {"category_display":"vid",
                                    "category_slug":"vid"}]}
        index_name = get_index_name(PROP)
        indexer = SearchIndexer(index_name)
        response = indexer.index_single_prop(data_to_index, data_to_index['id'])
        # print "Scoopwhoop Indexed Article Response: " + str(response)
        stats = response['status']
        self.assertIsNotNone(response)
        self.assertEqual(stats, 1)


    #10 edit article info - es (proper data sent, docid exists)
    def test_edit_article_2(self):

        '''

        :return:
        '''
        docid = '5694b6edit07dfc5072cb4bc'
        prop = PROP
        data_to_update = {"slug":"slug", "ar_url":"ar_url", "ar_name":"ar_name_edit",
                          "content":"content", "tags":["tags"], "fImgUrl":"fImgurl_edit",
                          "title":"title", "ar_id":"12", "sh_heading":"123",
                          "pub_date":"June 04, 2015 13:39:33",
                          "swcats":[{"category_display":"category_dis",
                                     "category_slug":"category_slug"},
                                    {"category_display":"vid",
                                     "category_slug":"vid"}]}
        index_name = get_index_name(prop)
        indexer = SearchIndexer(index_name)
        response = indexer.update_doc_prop(docid, data_to_update)
        # print "Scoopwhoop Edited Article Response: " + str(response)
        stats = response['status']
        self.assertIsNotNone(response)
        self.assertEqual(stats, 1)


    #11 edit article info - es (proper data sent, docid does not exist)
    def test_edit_article_3(self):

        '''

        :return:
        '''
        docid = '5694b6edit07idc5072cb4bc'
        prop = PROP
        data_to_update = {"slug":"slug", "ar_url":"ar_url", "ar_name":"ar_name_edit",
                          "content":"content", "tags":["tags"], "fImgUrl":"fImgurl_edit",
                          "title":"title", "ar_id":"12", "sh_heading":"123",
                          "pub_date":"June 04, 2015 13:39:33",
                          "swcats":[{"category_display":"category_dis",
                                     "category_slug":"category_slug"},
                                    {"category_display":"vid",
                                     "category_slug":"vid"}]}
        index_name = get_index_name(prop)
        indexer = SearchIndexer(index_name)
        response = indexer.update_doc_prop(docid, data_to_update)
        # print "Scoopwhoop Edited Article docid not present Response: " + str(response)
        stats = response['status']
        self.assertIsNotNone(response)
        self.assertEqual(stats, -1)


    #12 edit article info - es (data dict - missing field sent (ex : fImgUrl), docid exists)
    def test_edit_article_4(self):

        '''

        :return:
        '''
        docid = '5694b6edit07dfc5072cb4bc'
        prop = PROP
        data_to_update = {"slug":"slug", "ar_url":"ar_url", "ar_name":"ar_name_edit",
                          "content":"content", "tags":["tags"], "title":"title",
                          "ar_id":"12", "sh_heading":"123",
                          "pub_date":"June 04, 2015 13:39:33",
                          "swcats":[{"category_display":"category_dis",
                                     "category_slug":"category_slug"},
                                    {"category_display":"vid",
                                     "category_slug":"vid"}]}
        index_name = get_index_name(prop)
        indexer = SearchIndexer(index_name)
        response = indexer.update_doc_prop(docid, data_to_update)
        # print "Scoopwhoop Edited Article Missing field in data dict Response: " + str(response)
        stats = response['status']
        self.assertIsNotNone(response)
        self.assertEqual(stats, -1)


    #13 edit article info - es (data sent - extra field : version, docid exists)
    def test_edit_article_5(self):

        '''

        :return:
        '''
        docid = '5694b6edit07dfc5072cb4bc'
        prop = PROP
        data_to_update = {"slug":"slug", "ar_url":"ar_url", "ar_name":"ar_name_edit",
                          "version":"version", "content":"content-edit", "tags":["tags"],
                          "fImgUrl":"fImgurl_edit", "title":"title", "ar_id":"12",
                          "sh_heading":"123", "pub_date":"June 04, 2015 13:39:33",
                          "swcats":[{"category_display":"category_dis",
                                     "category_slug":"category_slug"},
                                    {"category_display":"vid",
                                     "category_slug":"vid"}]}
        index_name = get_index_name(prop)
        indexer = SearchIndexer(index_name)
        response = indexer.update_doc_prop(docid, data_to_update)
        # print "Scoopwhoop Edited Article containing extra field Response: " + str(response)
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
        data_to_update = {"slug":"slug", "ar_url":"ar_url", "ar_name":"ar_name_edit",
                          "content":[{"category_display":"category_dis",
                                      "category_slug":"category_slug"},
                                     {"category_display":"vid",
                                      "category_slug":"vid"}],
                          "tags":["tags"], "fImgUrl":"fImgurl_edit", "title":"title",
                          "ar_id":"12", "sh_heading":"123",
                          "pub_date":"June 04, 2015 13:39:33",
                          "swcats":[{"category_display":"category_dis",
                                     "category_slug":"category_slug"},
                                    {"category_display":"vid",
                                     "category_slug":"vid"}]}
        index_name = get_index_name(prop)
        indexer = SearchIndexer(index_name)
        response = indexer.update_doc_prop(docid, data_to_update)
        # print "Scoopwhoop Edited Article containing content
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
        data_to_update = {"slug":"slug", "ar_url":"ar_url", "ar_name":"ar_name_edit",
                          "content":"content", "tags":["tags"], "fImgUrl":"fImgurl_edit",
                          "title":"title", "ar_id":"12", "sh_heading":"123",
                          "pub_date":"Jan 04 2015 13:39",
                          "swcats":[{"category_display":"category_dis",
                                     "category_slug":"category_slug"},
                                    {"category_display":"vid",
                                     "category_slug":"vid"}]}
        index_name = get_index_name(prop)
        indexer = SearchIndexer(index_name)
        response = indexer.update_doc_prop(docid, data_to_update)
        # print "Scoopwhoop Edited Article with improper date format Response: " + str(response)
        stats = response['status']
        self.assertIsNotNone(response)
        self.assertEqual(stats, -1)


    #16 search published article - es // searchtype: for future,
    # can be article,category,author... ,
    def test_search_article_1(self):

        '''

        :return:
        '''
        qvar = 'scoopwhoop'
        pgnum = 1
        searchtype = ''
        sorttype = 'score'
        response = functiontosearch(qvar, pgnum, searchtype, sorttype)
        # print "Scoopwhoop Search Articles Response: " + str(response)
        stats = response['status']
        self.assertIsNotNone(response)
        self.assertEqual(stats, 1)

    #17 search published article - es // searchtype: for future,
    #  can be article,category,author... , pgnum=2
    def test_search_article_2(self):

        '''

        :return:
        '''
        qvar = 'scoopwhoop'
        pgnum = 2
        searchtype = ''
        sorttype = 'score'
        response = functiontosearch(qvar, pgnum, searchtype, sorttype)
        # print "Scoopwhoop Search Articles Response: " + str(response)
        stats = response['status']
        self.assertIsNotNone(response)
        self.assertEqual(stats, 1)


    #18 search published article - es // searchtype: for future,
    #  can be article,category,author... , sorttype=latest
    def test_search_article_3(self):

        '''

        :return:
        '''
        qvar = 'scoopwhoop'
        pgnum = 1
        searchtype = ''
        sorttype = 'latest'
        response = functiontosearch(qvar, pgnum, searchtype, sorttype)
        # print "Scoopwhoop Search Articles Response: " + str(response)
        stats = response['status']
        self.assertIsNotNone(response)
        self.assertEqual(stats, 1)


    #19 search published article - es // searchtype: for future,
    #  can be article,category,author... , pgnum=2, sorttype=latest
    def test_search_article_4(self):

        '''

        :return:
        '''
        qvar = 'sports'
        pgnum = 2
        searchtype = ''
        sorttype = 'latest'
        response = functiontosearch(qvar, pgnum, searchtype, sorttype)
        # print "Scoopwhoop Search Articles Response: " + str(response)
        stats = response['status']
        self.assertIsNotNone(response)
        self.assertEqual(stats, 1)


    #20 search published article - es // searchtype: for future,
    #  can be article,category,author... , pgnum=-1, sorttype=latest
    def test_search_article_5(self):

        '''

        :return:
        '''
        qvar = 'sports'
        pgnum = -1
        searchtype = ''
        sorttype = 'latest'
        response = functiontosearch(qvar, pgnum, searchtype, sorttype)
        # print "Scoopwhoop Search Articles Response: " + str(response)
        stats = response['status']
        self.assertIsNotNone(response)
        self.assertEqual(stats, 0)


    #21 search published article - es // searchtype: for future,
    #  can be article,category,author... , fuzzy match
    def test_search_article_6(self):

        '''

        :return:
        '''
        qvar = 'salmaan khan'
        pgnum = 1
        searchtype = ''
        sorttype = 'score'
        response = functiontosearch(qvar, pgnum, searchtype, sorttype)
        # print "Scoopwhoop Search Articles Response: " + str(response)
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
        qvar = 'scoopwhoop'
        pgnum = 1
        searchtype = ''
        sorttype = 'oldest'
        response = functiontosearch(qvar, pgnum, searchtype, sorttype)
        # print "Scoopwhoop Search Articles Response: " + str(response)
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
        qvar = 'scoopwhoop'
        pgnum = 0
        searchtype = ''
        sorttype = 'score'
        response = functiontosearch(qvar, pgnum, searchtype, sorttype)
        # print "Scoopwhoop Search Articles Response: " + str(response)
        stats = response['status']
        self.assertIsNotNone(response)
        self.assertEqual(stats, 0)


    #24 get mlt results : docid, category, prop
    def test_mlt_response_1(self):

        '''

        :return:
        '''
        xvar = function_to_get_id_cat_mlt()
        did = xvar['hits']['hits'][0]['_source']['id']
        dcategory = xvar['hits']['hits'][0]['_source']['swcats'][0]['category_slug']

        docid = did
        category = dcategory
        prop = PROP
        response = findmltdocsprop(docid, prop, category)
        # print "Scoopwhoop MLT Response: " + str(response)
        stats = response['status']
        self.assertIsNotNone(response)
        self.assertEqual(stats, 1)


    #25 get mlt results : docid, category, [prop : incorrect value/not given]
    def test_mlt_response_2(self):

        '''

        :return:
        '''
        xvar = function_to_get_id_cat_mlt()
        did = xvar['hits']['hits'][0]['_source']['id']
        dcategory = xvar['hits']['hits'][0]['_source']['swcats'][0]['category_slug']

        docid = did
        category = dcategory
        prop = 'anything'
        response = findmltdocsprop(docid, prop, category)
        # print "Scoopwhoop MLT Response: " + str(response)
        stats = response['status']
        self.assertIsNotNone(response)
        self.assertEqual(stats, 0)


    #26 get mlt results : docid, category : news, prop
    def test_mlt_response_3(self):

        '''

        :return:
        '''
        mod_time = datetime.now() + timedelta(days=-(2))
        dbac = datetime.strftime(mod_time, "%Y-%m-%d")

        xvar = function_to_get_id_cat_mlt()
        try:
            for inf in xvar['hits']['hits']:
                if {'category_display': "News",
                        'category_slug': "news"
                   } in inf['_source']['swcats']:
                    newsart = inf
                    break
        except Exception as exp:
            print str(exp)

        did = newsart['_source']['id']

        docid = did
        category = 'news'
        prop = PROP
        response = findmltdocsprop(docid, prop, category)
        # print "Scoopwhoop MLT Response: " + str(response)
        stats = response['status']
        info = response['info']
        try:
            for inf in info['hits']['hits']:
                print inf['_source']['date_sort']
                if inf['_source']['date_sort'] < dbac:
                    self.assertIsNone(inf['_source']['date_sort'])
        except Exception as exp:
            print str(exp)
        self.assertIsNotNone(response)
        self.assertEqual(stats, 1)


    #27 get mlt results : docid, category : news, prop
    def test_mlt_response_4(self):

        '''

        :return:
        '''
        xvar = function_to_get_id_cat_mlt()
        did = xvar['hits']['hits'][0]['_source']['id']
        dcategory = xvar['hits']['hits'][0]['_source']['swcats'][0]['category_slug']

        docid = did
        category = dcategory
        prop = PROP
        response = findmltdocsprop(docid, prop, category)
        # print "Scoopwhoop MLT Response: " + str(response)
        stats = response['status']
        info = response['info']
        try:
            for inf in info['hits']['hits']:
                self.assertNotIn({'category_display': "News",
                                  'category_slug': "news"}, inf['_source']['swcats'])
        except Exception as exp:
            print str(exp)
        self.assertIsNotNone(response)
        self.assertEqual(stats, 1)
