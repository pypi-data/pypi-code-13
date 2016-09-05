'''
__author__ = 'monica'
__author__ = 'chitraangi'

file to get the index alias name from the prop code.

'''

import json
from .defines import ES_DICT_PROPERTIES, ES_DICT_FIELD_PROPERTIES,\
    DEFAULT_FIELDS_DICT, ES_INDEX_MAPPING, ES_INDEX_SETTINGS
from .originals_defines import ES_DICT_PROPERTIES_ORI
from ..exceptions.loggerfileload import LOGGER_SEARCH


def get_index_name(code):
    '''

    :param code: based on the input, it returns the index name of the relevant property
    :return:
    '''

    try:

        #index_name = ES_DICT_PROPERTIES[code]

        if code == 'or05':
            index_name = ES_DICT_PROPERTIES_ORI[code]
            # print index_name
        elif code == '25rt' or code == '679a' or code == 's57v':
            index_name = ES_DICT_PROPERTIES[code]
            # print index_name
        else:
            index_name = 'index for this property does not exist'

    except KeyError:  ## by default lets get vb for now..
        index_name = None
        LOGGER_SEARCH.error(str(KeyError))

    return index_name


def get_fields_dict(code):
    '''

    :param code: based on the input, it returns the fields dict of the relevant property
    :return:
    '''

    try:

        f_dict = ES_DICT_FIELD_PROPERTIES[code]

    except KeyError:  ## by default lets get vb for now..
        f_dict = DEFAULT_FIELDS_DICT

    return f_dict


def get_mapping(data):
    '''

    :param code: based on the input, it returns the index name of the relevant property
    :return:
    '''

    if data.has_key('mapping'):
        if data['mapping'] != None:
            index_mapping = json.loads(data['mapping'])
            return index_mapping

    return ES_INDEX_MAPPING


def get_setting(data):
    '''

    :param code: based on the input, it returns the index name of the relevant property
    :return:
    '''

    if data.has_key('setting'):
        if data['setting'] != None:
            index_setting = json.loads(data['setting'])
            return index_setting

    return ES_INDEX_SETTINGS
