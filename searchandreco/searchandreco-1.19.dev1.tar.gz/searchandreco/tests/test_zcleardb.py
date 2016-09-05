'''
__author__ : 'chitraangi'

'''

from .base import SearchDbTestCase
from ..eswrapper.utils import get_index_name
from ..eswrapper.eswrapper import SearchIndexer
from ..eswrapper.originals_eswrapper import SearchIndexerOriginals

## the prop value for scoopwhoop is 25rt
SW_PROP = '25rt'
VB_PROP = '679a'
OR_PROP = 'or05'

class TestCleardb(SearchDbTestCase):

    '''
    #1 remove db created
    '''

    def test_z_zremove_al_data_created(self):

        '''
        #1 remove db created
        :return:
        '''
        index_name = get_index_name(SW_PROP)
        indexer = SearchIndexer(index_name)

        docid = '5694b6aa2d07dfc5072cb4bc'
        indexer.delete_doc(docid)

        docid_extra = '7694b6aa2d07dfc5072cb4bc'
        indexer.delete_doc(docid_extra)

        docid_edit = '5694b6edit07dfc5072cb4bc'
        indexer.delete_doc(docid_edit)

        index_name_vb = get_index_name(VB_PROP)
        indexer_vb = SearchIndexer(index_name_vb)

        docid_v = '1694b6aa2d07dfc5072cb4bc'
        indexer_vb.delete_doc(docid_v)

        docid_extra_v = '7694b6aa2d07dfc5072cb4bc'
        indexer_vb.delete_doc(docid_extra_v)

        docid_edit_v = '5694b6edit07dfc5072cb4bc'
        indexer_vb.delete_doc(docid_edit_v)

        index_name_ori = get_index_name(OR_PROP)
        indexer_ori = SearchIndexerOriginals(index_name_ori)

        docid_or = '5694b6aa2d07dfc5072cb4an'
        indexer_ori.delete_doc_originals(docid_or)

        docid_extra_or = '5694b6aa2d07dfc5072cbkan'
        indexer_ori.delete_doc_originals(docid_extra_or)

        docid_edit_or = 'ch94b6edit07dfc5072cb4bc'
        indexer_ori.delete_doc_originals(docid_edit_or)

        docid_edit_or_2 = '9694b6edit07dfc5072cb4bc'
        indexer_ori.delete_doc_originals(docid_edit_or_2)

