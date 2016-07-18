import re
from terminaltables import AsciiTable
from textwrap import wrap

from .sently_resource_mapping import RESOURCE_MAPPING as sently
from .gsheets_resource_mapping import RESOURCE_MAPPING as gsheets
from .gmail_resource_mapping import RESOURCE_MAPPING as gmail
from .spotify_resource_mapping import RESOURCE_MAPPING as spotify
from .youtube_resource_mapping import RESOURCE_MAPPING as youtube

def sentlyinfo():
    table_instance = create_table(sently)
    print(table_instance.table)

def gsheetsinfo():
    table_instance = create_table(gsheets)
    print(table_instance.table)

def gmailinfo():
    table_instance = create_table(gmail)
    print(table_instance.table)

def spotifyinfo():
    table_instance = create_table(spotify)
    print(table_instance.table)

def youtubeinfo():
    table_instance = create_table(youtube)
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
