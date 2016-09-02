'''
__author__ : 'chitraangi'

'''

from .base import SearchDbTestCase
from ..eswrapper.utils import get_index_name
from ..eswrapper.eswrapper import SearchIndexer

## the prop value for scoopwhoop is 25rt
SW_PROP = '25rt'

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
