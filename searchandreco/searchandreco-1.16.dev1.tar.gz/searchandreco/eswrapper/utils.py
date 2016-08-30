__author__ = 'monica'

import json
from defines import *
from originals_defines import *

def get_index_name(code):

    '''

    :param code: based on the input, it returns the index name of the relevant property
    :return:
    '''

    try:

        #index_name = ES_DICT_PROPERTIES[code]
	
	if code == 'or05' : 
		index_name = ES_DICT_PROPERTIES_ORI[code]
		print index_name
	else :
		index_name = ES_DICT_PROPERTIES[code]

    except KeyError:## by default lets get vb for now..
        index_name = None

    return index_name

def get_fields_dict(code):

    '''

    :param code: based on the input, it returns the fields dict of the relevant property
    :return:
    '''

    try:

        f_dict = ES_DICT_FIELD_PROPERTIES[code]

    except KeyError:## by default lets get vb for now..
        f_dict = DEFAULT_FIELDS_DICT

    return f_dict


def get_mapping(data):

    '''

    :param code: based on the input, it returns the index name of the relevant property
    :return:
    '''

    if(data.has_key('mapping')):
        if(data['mapping'] != None):
            index_mapping = json.loads(data['mapping'])
            return index_mapping

    return ES_INDEX_MAPPING

def get_setting(data):

    '''

    :param code: based on the input, it returns the index name of the relevant property
    :return:
    '''

    if(data.has_key('setting')):
        if(data['setting'] != None):
            index_setting = json.loads(data['setting'])
            return index_setting

    return ES_INDEX_SETTINGS


def modify_querystring(qstr):

    '''

    :param code: based on the input, it modies the query string
    :return:
    '''

    schars = [ "'", "#", "!", "%", "^", "&", "(", ")", "+", "{", "}", "\\", ":",";","\"", "<", ">", "?", "/" ]

    for sch in schars :
	if qstr.find("'s") :
            qstr = qstr.replace("'s","")
        elif qstr.find(sch) or qstr[0] == sch:
            qstr = qstr.replace(sch," ")
    # print qstr
    return qstr
