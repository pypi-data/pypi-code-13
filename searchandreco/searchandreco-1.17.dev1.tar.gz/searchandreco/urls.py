'''
__author__ = 'monica'
__author__ = 'monica'

The end points
'''



URLS = (

    '/', 'Home',
    ## we need to ensure that the reuqest come only respective IP// Not open
    '/create_index/', 'CreateIndex',
    ## we need to ensure that the reuqest come only respective IP// Not open
    '/exists/', 'IndexExists',
    '/delete_doc/', 'DeleteDocument',
    '/index_doc/', 'IndexSingle',
    '/update_doc/', 'UpdateDocument',

    ###added urls
    '/removeunpublisheddrafts', 'RemoveUnpublishedArticles',
    '/indexpublisheddraftsprop', 'IndexPublishedDraftsArticlesProp',
    '/updatedocumentprop', 'UpdateArticlesDocumentProp',

    '/searchuserfacingsw', 'SearchSWUserFacing',
    '/searchuserfacingvb', 'SearchVBUserFacing',
    '/searchuserfacinggp', 'SearchGPUserFacing',

    '/mltdocsprop', 'MltDocProp',

    ####originals
    '/indexoriginals', 'IndexOriginals',
    '/mltoriginals', 'MltOriginals',
    '/updateoriginals', 'UpdateOriginals',
    '/deleteoriginals', 'DeleteOriginals',
    '/searchuserfacingoriginals', 'SearchORIGINALSUserFacing'

)
