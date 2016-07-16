import requests
import re
import os
from terminaltables import AsciiTable
from textwrap import wrap

from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run_flow, argparser
from oauth2client.file import Storage
from oauth2client import tools

from .sently_resource_mapping import RESOURCE_MAPPING as sently
from .gsheets_resource_mapping import RESOURCE_MAPPING as gsheets
from .gmail_resource_mapping import RESOURCE_MAPPING as gmail

def sentlyinfo():
    table_instance = create_table(sently)
    print(table_instance.table)

def gsheetsinfo():
    table_instance = create_table(gsheets)
    print(table_instance.table)

def gmailinfo():
    table_instance = create_table(gmail)
    print(table_instance.table)


def create_table(res_map):
    table_data = [['function', 'path_params', 'methods', 'query_params / body']]
    max_width = 30
    _data = []
    for key, value in res_map.items():
        _function = key
        pp = re.findall(r"\{(\w+)\}", value['resource'])
        _path_params = ''
        if pp:
            _path_params = ",\n".join(pp)
        _methods = ",\n".join(value['methods'])
        _remarks = '\n'.join(wrap(value['remarks'], 30))
        _data.append([_function, _path_params, _methods, _remarks])

    table_data.extend(_data)
    table_instance = AsciiTable(table_data)
    table_instance.inner_heading_row_border = True
    table_instance.inner_row_border = True
    return table_instance

def google_auth(client_id, client_secret, scope):
    flow = OAuth2WebServerFlow(client_id=client_id,
                           client_secret=client_secret,
                           scope=scope,
                           redirect_uri='http://localhost')
    storage = Storage('creds.data')
    flags = argparser.parse_args(args=[])
    credentials = run_flow(flow, storage, flags)
    access_token = credentials.access_token
    os.remove('creds.data')
    return access_token
