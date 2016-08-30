__author__ = 'monica'



urls = (

    '/', 'Home',
    '/create_index/', 'CreateIndex', ## we need to ensure that the reuqest come only respective IP// Not open
    '/exists/', 'IndexExists', ## we need to ensure that the reuqest come only respective IP// Not open
    '/delete_doc/', 'DeleteDocument',
    '/index_doc/', 'IndexSingle',
    '/update_doc/', 'UpdateDocument',

    ###added urls
    '/removeunpublisheddrafts','RemoveUnpublishedArticles',

    '/searchuserfacingsw','SearchSWUserFacing',

    '/searchpubdrftauth','SearchSWPubDrftAuth',

    '/mltdocfinal','MltDocFinal',

    '/indexpublisheddraftsprop','IndexPublishedDraftsArticlesProp',
    '/updatedocumentprop','UpdateArticlesDocumentProp',

    '/searchuserfacingvb','SearchVBUserFacing',

    '/mltdocsprop','MltDocProp',

    '/create_index_gp/','CreateIndexGP',

    '/searchuserfacinggp','SearchGPUserFacing',


    ####originals
    '/indexoriginals','IndexOriginals',
    '/mltoriginals','MltOriginals',
    '/updateoriginals','UpdateOriginals',
    '/deleteoriginals','DeleteOriginals',
    '/searchuserfacingoriginals','SearchORIGINALSUserFacing'




)
