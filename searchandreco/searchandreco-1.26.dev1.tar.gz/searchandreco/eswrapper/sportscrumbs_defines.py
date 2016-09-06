'''
__author__ = 'chitraangi'
'''

USE_NO_MAPPING = 0
USE_MAPPING = 1

MAPPING_TYPE = USE_MAPPING

# fields to be index
# - title
# - slug
# - author name (public name)
# - content
# - published date
# - tags
# - categories
# - hashtags
# - co-author names
# - DB Id
# - Redis Id
# - Version Number
# - short heading
# - description
# - introduction

ES_FIELD_ID = 'id'
ES_FIELD_SLUG = 'slug'
ES_FIELD_TITLE = 'title'
ES_FIELD_FI_URL = 'fImgUrl'
ES_FIELD_SH_HEADING = 'sh_heading'
ES_FIELD_AUTHOR_NAME = 'ar_name'
ES_FIELD_COAUTHOR_NAMES = 'co_ar_name'
ES_FIELD_PUB_DATE = 'pub_date'
ES_FIELD_DB_ID = 'db_id'
ES_FIELD_REDIS_ID = 'r_id'
ES_FIELD_VERSION_NO = 'v_no'
ES_FIELD_TAGS = 'tags'
ES_FIELD_CATS = 'cats'
ES_FIELD_HTAGS = 'hashtags'
ES_FIELD_AUTHOR_USERNAME = 'ar_uname'
ES_FIELD_COAUTHOR_USERNAME = 'co_ar_uname'
#ES_FIELD_DESCRIPTION = 'descr'
ES_FIELD_INTRODUCTION = 'intro'
ES_FIELD_CONTENT = 'content'
ES_FIELD_TYPE = 'type'
ES_FIELD_SUBTYPE = 'subtype'

ES_FIELD_PARA_TITLES = 'para_titles'
ES_FIELD_PARA_DETAILS = 'para_details'

##added fields for SW
ES_FIELD_SWCATS = 'swcats'
ES_FIELD_CAT_SLUG = 'category_slug'
ES_FIELD_DIS_NAME = 'category_display'
ES_FIELD_AR_ID = 'ar_id'
ES_FIELD_AR_URL = 'ar_url'
ES_FIELD_DATE_SORT = 'date_sort'

ES_FIELD_TEAM = 'team'
ES_FIELD_SPORT = 'sport'
ES_FIELD_ACTION = 'action'
ES_FIELD_PLAYER = 'player'

STOPWORDS = 'a,able,about,across,after,all,almost,also,am,among,an,and,any,are,as,at,be,because, \
been,but,by,can,cannot,could,dear,did,do,does,either,else,ever,every,for,from,get,got, \
had,has,have,he,her,hers,him,his,how,however,i,if,in,into,is,it,its,just,least,let,like,likely, \
may,me,might,most,must,my,neither,no,nor,not,of,off,often,on,only,or,other,our,own,rather,said,say,says, \
she,should,since,so,some,than,that,the,their,them,then,there,these,they,this,tis,to,too,twas,us,wants,was,we, \
were,what,when,where,which, while,who,whom,why,will,with,would,yet,you,your'

ES_MLT_STOPWORDS = STOPWORDS.split(',')

ES_CONTENT_DOC_TYPE_SPRTCRMBS = 'post'

## This setting is not the final one.. Just for trial as of now

ES_FULL_TEXT_ANALYZER = "fulltext_analyzer"

ES_FULL_TEXT_ANALYZER_RULES = {"type": "standard",
                               "stopwords": ES_MLT_STOPWORDS,
                               "filter": ["lowercase", "apostrophe",
                                          "asciifolding"],
                               "tokenizer": "whitespace",
                               "char_filter": ["html_strip"]}

ES_ANALYZER = {"analyzer": {ES_FULL_TEXT_ANALYZER: ES_FULL_TEXT_ANALYZER_RULES}
              }

ES_INDEX_SETTINGS = {"analysis": ES_ANALYZER}


ES_INDEX_MAPPING = {
    ES_CONTENT_DOC_TYPE_SPRTCRMBS: {
        'properties': {
            ES_FIELD_ID: {'type': 'string', 'null_value':'na',\
                          'store': True, 'index': 'not_analyzed'},
            ES_FIELD_TITLE: {'type': 'string', 'store': True,\
                             "term_vector": "with_positions_offsets_payloads"},
            ES_FIELD_SLUG: {'type': 'string', 'store': True,\
                            'index': 'not_analyzed'},
            ES_FIELD_TYPE: {'type': 'string', 'store': True},
            ES_FIELD_SUBTYPE: {'type': 'string', 'store': True},
            ES_FIELD_FI_URL: {'type': 'string', 'store': True,\
                              'null_value':'na', 'index': 'not_analyzed'},

            ES_FIELD_SH_HEADING: {'type': 'string', 'store': True, 'null_value':'na'},
            ES_FIELD_AUTHOR_NAME: {'type': 'string', 'store': True, 'null_value':'na'},
            ES_FIELD_AR_ID:{'type': "string", 'store': True,\
                             'null_value': 'na', 'index': 'not_analyzed'},
            ES_FIELD_AR_URL:{'type': "string", 'store': True,\
                             'null_value': 'na', 'index': 'not_analyzed'},
            ES_FIELD_COAUTHOR_NAMES: {'type': 'string', 'store': True,\
                                      'null_value':'na'},
            ES_FIELD_PUB_DATE: {'type': 'string', 'null_value':'na',\
                                'store': True, 'index': 'not_analyzed'},
            ES_FIELD_DATE_SORT : {'type': "date", 'format': "yyyy-MM-dd"},
            #ES_FIELD_DB_ID: {'type': 'string', 'null_value':'na',
            #  'store': True,  'index': 'not_analyzed'},
            ES_FIELD_REDIS_ID: {'type': 'integer', 'store': True,\
                                'index': 'not_analyzed'}, ## ?? required or not
            ## a custom analyzer may be required for tokenizing on commas
            ES_FIELD_VERSION_NO: {'type': 'integer', 'analyzer': 'keyword',\
                                  'store': True, 'index': 'not_analyzed'},
            ES_FIELD_TAGS: {'type': 'string', 'store': True,\
                            "term_vector": "with_positions_offsets_payloads"},
            ES_FIELD_TEAM:{'type': 'string', 'store': True,\
                           "term_vector": "with_positions_offsets_payloads"},
            ES_FIELD_SPORT:{'type': 'string', 'store': True,\
                            "term_vector": "with_positions_offsets_payloads"},
            ES_FIELD_ACTION:{'type': 'string', 'store': True,\
                             "term_vector": "with_positions_offsets_payloads"},
            ES_FIELD_PLAYER:{'type': 'string', 'store': True,\
                             "term_vector": "with_positions_offsets_payloads"},
            ## a custom analyzer may be required for tokenizing on commas
            ES_FIELD_CATS: {'type': 'string', 'store': True,\
                            "term_vector": "with_positions_offsets_payloads"},
            ##mapping added SW
            ES_FIELD_SWCATS: {
                'properties' : {
                    ES_FIELD_CAT_SLUG : {'type': 'string', 'store': True,\
                                         'index': 'not_analyzed'},
                    ES_FIELD_DIS_NAME : {'type': 'string',\
                                         'store': True,\
                                         "term_vector": "with_positions_offsets_payloads"}
                }
            },
            ES_FIELD_HTAGS: {'type': 'string', 'analyzer': 'keyword', 'null_value': 'na'},
            ES_FIELD_AUTHOR_USERNAME: {'type': 'string', 'store': True, 'index': 'not_analyzed'},
            ES_FIELD_COAUTHOR_USERNAME: {'type': 'string', 'store': True,\
                                         'index': 'not_analyzed', 'null_value':'na'},
            ## description is same as short heading hence commented for now.
            #ES_FIELD_DESCRIPTION: {'type': 'string',
            #  'store': True, 'analyzer': 'keyword', 'null_value':'na'},
            ES_FIELD_INTRODUCTION: {'type': 'string', 'store': True,\
                                    'analyzer': 'keyword', 'null_value':'na'},
            ES_FIELD_CONTENT: {'type': 'string', 'store': True, 'null_value':'na'},
            ES_FIELD_PARA_TITLES: {'type': 'string', 'store': True, 'null_value':'na'},
            ES_FIELD_PARA_DETAILS: {'type': 'string', 'store': True, 'null_value':'na'},
            "title-suggest" : {
                "type" : "completion",
                "index_analyzer" : "fulltext_analyzer",
                "search_analyzer" : "simple",
                "payloads" : "true",
                "preserve_position_increments" : "false",
                "preserve_separators": "false"
            },
            "team-suggest" : {
                "type" : "completion",
                "index_analyzer" : "fulltext_analyzer",
                "search_analyzer" : "simple",
                "payloads" : "true",
                "preserve_position_increments" : "false",
                "preserve_separators": "false"
            },
            "sport-suggest" : {
                "type" : "completion",
                "index_analyzer" : "fulltext_analyzer",
                "search_analyzer" : "simple",
                "payloads" : "true",
                "preserve_position_increments" : "false",
                "preserve_separators": "false"
            },
            "action-suggest" : {
                "type" : "completion",
                "index_analyzer" : "fulltext_analyzer",
                "search_analyzer" : "simple",
                "payloads" : "true",
                "preserve_position_increments" : "false",
                "preserve_separators": "false"
            },
            "player-suggest" : {
                "type" : "completion",
                "index_analyzer" : "fulltext_analyzer",
                "search_analyzer" : "simple",
                "payloads" : "true",
                "preserve_position_increments" : "false",
                "preserve_separators": "false"
            }
        },
        '_timestamp' : {
            "enabled" : True,
            "format" : 'basic_ordinal_date_time'
        }
    }
}

###index list
SC_INDEX_LIST = ['spcrmbs_realtimeposts_alias']

ES_DICT_PROPERTIES_SPRTCRMBS = {'sp99': 'spcrmbs_realtimeposts_alias'}

SPRTCRMBS = 'sp99'
