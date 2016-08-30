from base import *
from ..eswrapper.utils import *
from ..eswrapper.eswrapper import *

## the prop value for scoopwhoop is 25rt
SW_PROP = '25rt'

class TestCleardb(SearchDbTestCase):

	#1 remove db created
	def test_z_ZremoveAllDataCreated(self) :

		index_name = get_index_name(SW_PROP)
		indexer = SearchIndexer(index_name)

		docid = '5694b6aa2d07dfc5072cb4bc'
		response = indexer.delete_doc(docid)

		docid_extra = '7694b6aa2d07dfc5072cb4bc'
		response = indexer.delete_doc(docid_extra)

		docid_edit = '5694b6edit07dfc5072cb4bc'
		response = indexer.delete_doc(docid_edit)