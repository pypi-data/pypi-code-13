__author__ = 'monica'

from settings import GP_STOPWORDS_FILE_NAME

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



ES_CONTENT_DOC_TYPE = 'post'

## This setting is not the final one.. Just for trial as of now

ES_FULL_TEXT_ANALYZER = "fulltext_analyzer"

ES_FULL_TEXT_ANALYZER_RULES = {

          "type": "custom",
          "tokenizer": "whitespace",
          "filter": [
            "lowercase"
#            "type_as_payload"
          ]

}

ES_ANALYZER = { "analyzer": {ES_FULL_TEXT_ANALYZER : ES_FULL_TEXT_ANALYZER_RULES}}

ES_INDEX_SETTINGS = {

    # "index" : {
    #      "number_of_shards" : 1,
    #     "number_of_replicas" : 0
    # },

    "analysis" : ES_ANALYZER
}


######gazabpost settings

ES_INDEX_SETTINGS_GP = {

        "analysis": {

        "filter" : {

            "stopwords_filter" : {

                "type" : "stop",
                "stopwords" : ["http", "https", "ftp", "www"]
            },

            ## hindi related
            "hindi_stop": {
                "type":       "stop",
                # "stopwords":  "_hindi_",
                "stopwords_path": GP_STOPWORDS_FILE_NAME
            },

            # "hindi_keywords": {
            #     "type":       "keyword_marker",
            #     "keywords":   []
            # },

            "hindi_stemmer": {
                "type":       "stemmer",
                "language":   "hindi"
            }


      },
        "analyzer": {

            "url_analyzer": {
                "type": "custom",
                "tokenizer": "lowercase",
                "filter": [ "stopwords_filter" ]
            },


            "hindi": {

                "tokenizer":  "standard",

                "filter": [
                    "lowercase",
                    "indic_normalization",
                    "hindi_normalization",
                    "hindi_stop",
                    #"hindi_keywords",
                    #"hindi_stemmer"  ## not using stemmer for now...
                ]
            }

      }
    }
}



ES_INDEX_MAPPING = {

    ES_CONTENT_DOC_TYPE: {

        'properties': {

            ES_FIELD_ID: {'type': 'string','null_value':'na', 'store': True, 'index': 'not_analyzed'},
            ES_FIELD_TITLE: {'type': 'string', 'store': True, "term_vector": "with_positions_offsets_payloads"},
            ES_FIELD_SLUG: {'type': 'string','store': True, 'index': 'not_analyzed'},
            ES_FIELD_TYPE: {'type': 'string', 'store': True},
            ES_FIELD_SUBTYPE: {'type': 'string', 'store': True},
            ES_FIELD_FI_URL: {'type': 'string','store': True, 'null_value':'na', 'index': 'not_analyzed'},

            ES_FIELD_SH_HEADING: {'type': 'string', 'store': True,'null_value':'na'},
            ES_FIELD_AUTHOR_NAME: {'type': 'string', 'store': True, 'null_value':'na'},
            ES_FIELD_AR_ID:{ 'type': "string",'store': True,'null_value': 'na', 'index': 'not_analyzed'},
            ES_FIELD_AR_URL:{'type': "string",'store': True,'null_value': 'na', 'index': 'not_analyzed'},
            ES_FIELD_COAUTHOR_NAMES: {'type': 'string', 'store': True, 'null_value':'na'},
            ES_FIELD_PUB_DATE: {'type': 'string', 'null_value':'na', 'store': True,  'index': 'not_analyzed'},
            ES_FIELD_DATE_SORT : {'type': "date",'format': "yyyy-MM-dd"},
            #ES_FIELD_DB_ID: {'type': 'string', 'null_value':'na', 'store': True,  'index': 'not_analyzed'},
            ES_FIELD_REDIS_ID: {'type': 'integer',  'store': True, 'index': 'not_analyzed'}, ## ?? required or not
            ES_FIELD_VERSION_NO: {'type': 'integer', 'analyzer': 'keyword', 'store': True, 'index': 'not_analyzed'},
            ES_FIELD_TAGS: {'type': 'string', 'store': True, "term_vector": "with_positions_offsets_payloads"}, ## a custom analyzer may be required for tokenizing on commas
            ES_FIELD_CATS: {'type': 'string', 'store': True, "term_vector": "with_positions_offsets_payloads"}, ## a custom analyzer may be required for tokenizing on commas
            ##mapping added SW
            ES_FIELD_SWCATS: {
                'properties' : {
                                ES_FIELD_CAT_SLUG : {'type': 'string', 'store': True, 'index': 'not_analyzed'},
                                ES_FIELD_DIS_NAME : {'type': 'string', 'store': True, "term_vector": "with_positions_offsets_payloads"}
                        }
                        },
            ES_FIELD_HTAGS: {'type': 'string', 'analyzer': 'keyword', 'null_value': 'na'},
            ES_FIELD_AUTHOR_USERNAME: {'type': 'string', 'store': True, 'index': 'not_analyzed'},
            ES_FIELD_COAUTHOR_USERNAME: {'type': 'string', 'store': True, 'index': 'not_analyzed', 'null_value':'na'},
            ## description is same as short heading hence commented for now.
            #ES_FIELD_DESCRIPTION: {'type': 'string', 'store': True, 'analyzer': 'keyword', 'null_value':'na'},
            ES_FIELD_INTRODUCTION: {'type': 'string', 'store': True, 'analyzer': 'keyword', 'null_value':'na'},
            ES_FIELD_CONTENT: {'type': 'string', 'store': True, 'null_value':'na'},
            ES_FIELD_PARA_TITLES: {'type': 'string', 'store': True, 'null_value':'na'},
            ES_FIELD_PARA_DETAILS: {'type': 'string', 'store': True, 'null_value':'na'}

        },
        '_timestamp' : {
            "enabled" : True,
            "format" : 'basic_ordinal_date_time'
            }
    }
    }


###index list
SW_INDEX_LIST = ['swp_realtimeposts_alias']
VB_INDEX_LIST = ['vb_realtimeposts_alias']
GP_INDEX_LIST = ['gp_realtimeposts']


## can always modify these as they are being used during query time.

DEFAULT_FIELDS_DICT = {
                        ES_FIELD_TITLE      : 5,
                        ES_FIELD_CATS: 5,
                        ES_FIELD_TAGS: 5,
                        ES_FIELD_SH_HEADING : 4,
                        ES_FIELD_AUTHOR_NAME: 4,
                        ES_FIELD_COAUTHOR_NAMES: 4,
                        ES_FIELD_INTRODUCTION: 4,
                        ES_FIELD_CONTENT : 4,


                      }

DEFAULT_SWP_FIELDS_DICT = {
                        ES_FIELD_TAGS: 6,
                        ES_FIELD_TITLE      : 6,
                        ES_FIELD_CONTENT : 5,
                        ES_FIELD_AUTHOR_NAME: 4,
                        ES_FIELD_DIS_NAME: 3,
                        ES_FIELD_SH_HEADING : 3,

                      }

DEFAULT_VB_FIELDS_DICT = {
                        ES_FIELD_TAGS: 6,
                        ES_FIELD_TITLE      : 6,
                        ES_FIELD_CONTENT : 5,
                        ES_FIELD_AUTHOR_NAME: 4,
                        ES_FIELD_DIS_NAME: 1,
                        ES_FIELD_SH_HEADING : 1,

                      }

DEFAULT_SWP_FIELDS_DICT_ARTICLE = {
                        ES_FIELD_TAGS: 5,
                        ES_FIELD_TITLE      : 5,
                        ES_FIELD_CONTENT : 5,
                        ES_FIELD_SH_HEADING : 4,
                        ES_FIELD_CATS: 4,

                      }

ES_MLT_MIN_TERM_FREQ = 1
ES_MLT_MAX_QUERY_TERMS = 5

ES_MLT_FIELDS = ",".join([ES_FIELD_TAGS, ES_FIELD_TITLE ])

ES_MLT_LIMIT = 5


STOPWORDS = 'a,able,about,across,after,all,almost,also,am,among,an,and,any,are,as,at,be,because, \
been,but,by,can,cannot,could,dear,did,do,does,either,else,ever,every,for,from,get,got, \
had,has,have,he,her,hers,him,his,how,however,i,if,in,into,is,it,its,just,least,let,like,likely, \
may,me,might,most,must,my,neither,no,nor,not,of,off,often,on,only,or,other,our,own,rather,said,say,says, \
she,should,since,so,some,than,that,the,their,them,then,there,these,they,this,tis,to,too,twas,us,wants,was,we, \
were,what,when,where,which, while,who,whom,why,will,with,would,yet,you,your'

ES_MLT_STOPWORDS = STOPWORDS.split(',')



## Just writing a few for now
#ES_MLT_STOPWORDS = ["what", "where", "when", "is", "was", "for", "you", "were", "are", "this", "that", "which", "the","a", "an" ]

ES_DICT_PROPERTIES = {'679a': 'vb_realtimeposts_alias', '53e4': 'swp_posts', 'f30a': 'gp_posts',\
                      '25rt': 'swp_realtimeposts_alias', 'd90f': 'swp_realtimedrafts', 's57v': 'gp_realtimeposts'} ###modified #vb_posts changed to vb_realtimeposts
ES_DICT_FIELD_PROPERTIES = {'679a': DEFAULT_FIELDS_DICT, '53e4': DEFAULT_SWP_FIELDS_DICT, 'f30a': DEFAULT_FIELDS_DICT,\
                            '25rt': DEFAULT_SWP_FIELDS_DICT, 'd90f': DEFAULT_SWP_FIELDS_DICT, 's57v':DEFAULT_VB_FIELDS_DICT} ###modified

VB = '679a'

SWP = '53e4'

GP  = 'f30a'

VBQ = 'vbq'

SWHPQ = 'swpq'

GPQ = 'gpq'



###  adding new index for realtime published articles and also adding it to ES_DICT_PROPERTIES
SWPRTPUB = '25rt'

SWDRFTS = 'd90f'

GPRT = 's57v'
