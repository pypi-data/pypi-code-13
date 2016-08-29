__author__ = 'chitraangi'

# -*- coding: utf-8 -*-

# fields to be index
# - slug
# - title
# - fimg url
# - short heading
# - author name (public name)
# - published field in (yyyy-mm-dd) format
# - published date
# - tags
# - content
# - author url


ES_FIELD_SH_HEADING = 'sh_heading'
ES_FIELD_AR_ID = 'ar_id'
ES_FIELD_TITLE = 'title'
ES_FIELD_FI_URL = 'fImgUrl'
ES_FIELD_TAGS = 'tags'
ES_FIELD_AUTHOR_NAME = 'ar_name'
ES_FIELD_AUTHOR_URL = 'ar_url'
ES_FIELD_PUB_DATE = 'pub_date'
ES_FIELD_SLUG = 'slug'
ES_FIELD_DATE_SORT = 'date_sort'
ES_FIELD_ID = 'id'
ES_FIELD_FLAG = 'flag'


ES_CONTENT_DOC_TYPE = 'post'


STOPWORDS = 'a,able,about,across,after,all,almost,also,am,among,an,and,any,are,as,at,be,because, \
been,but,by,can,cannot,could,dear,did,do,does,either,else,ever,every,for,from,get,got, \
had,has,have,he,her,hers,him,his,how,however,i,if,in,into,is,it,its,just,least,let,like,likely, \
may,me,might,most,must,my,neither,no,nor,not,of,off,often,on,only,or,other,our,own,rather,said,say,says, \
she,should,since,so,some,than,that,the,their,them,then,there,these,they,this,tis,to,too,twas,us,wants,was,we, \
were,what,when,where,which, while,who,whom,why,will,with,would,yet,you,your'

ES_MLT_STOPWORDS = STOPWORDS.split(',')



ES_FULL_TEXT_ANALYZER = "fulltext_analyzer"


ES_FULL_TEXT_ANALYZER_RULES = {
          "type": "custom",
          #"stopwords": ES_MLT_STOPWORDS,
        "filter": [
            "lowercase", "apostrophe", "asciifolding"
          ],
    "tokenizer": "whitespace",
            "char_filter": [
            "html_strip"
          ]
}

ES_ANALYZER = { "analyzer": {ES_FULL_TEXT_ANALYZER : ES_FULL_TEXT_ANALYZER_RULES}}


ES_INDEX_SETTINGS_ORIGINALS = {
    "analysis" : ES_ANALYZER
}


ES_INDEX_MAPPING_ORIGINALS = {
    ES_CONTENT_DOC_TYPE: {
        'properties': {
            ES_FIELD_SH_HEADING: {'type': 'string', 'store': True,'null_value':'na'},
            ES_FIELD_AR_ID:{ 'type': "string",'store': True,'null_value': 'na' , 'index': 'not_analyzed'},
            ES_FIELD_TITLE: {'type': 'string', 'store': True, "term_vector": "with_positions_offsets_payloads"},
            ES_FIELD_FI_URL: {'type': 'string','store': True, 'null_value':'na', 'index': 'not_analyzed'},
            ES_FIELD_TAGS: {'type': 'string', 'store': True, "term_vector": "with_positions_offsets_payloads"}, ## a custom analyzer may be required for tokenizing on commas
            ES_FIELD_AUTHOR_NAME:{'type': 'string', 'store': True, "term_vector": "with_positions_offsets_payloads"},
            ES_FIELD_AUTHOR_URL:{ 'type': "string",'store': True,'null_value': 'na' , 'index': 'not_analyzed'},
            ES_FIELD_PUB_DATE: {'type': 'string', 'null_value':'na', 'store': True,  'index': 'not_analyzed'},
            ES_FIELD_SLUG: {'type': 'string','store': True, 'index': 'not_analyzed'},
            ES_FIELD_DATE_SORT : {'type': "date",'format': "yyyy-MM-dd"},
            ES_FIELD_ID: {'type': 'string','null_value':'na', 'store': True, 'index': 'not_analyzed'},
	    ES_FIELD_FLAG: {'type': 'integer','store': True, 'index': 'not_analyzed'},

        }
    }
    }

SWORI_INDEX_LIST = ['swp_originalsposts_alias']



ES_MLT_MIN_TERM_FREQ = 1
ES_MLT_MAX_QUERY_TERMS = 5

ES_MLT_FIELDS = ",".join([ES_FIELD_TAGS, ES_FIELD_TITLE ])

ES_MLT_LIMIT = 5



ES_DICT_PROPERTIES_ORI = {'or05':'swp_originalsposts_alias'}


SWPORIG = 'or05'
