from terminaltables import AsciiTable
from textwrap import wrap
from .sently_resource_mapping import RESOURCE_MAPPING as sently
from .gsheets_resource_mapping import RESOURCE_MAPPING as gsheets

def sentlyinfo():
    table_instance = create_table(sently)
    print(table_instance.table)

def gsheetsinfo():
    table_instance = create_table(gsheets)
    print(table_instance.table)


def create_table(res_map):
    table_data = [['function', 'path_params', 'methods', 'query_params / body']]
    max_width = 30
    _data = []
    for key, value in res_map.items():
        _function = key
        _path_params = ''
        if value['path_params']:
            _path_params = ",\n".join(value['path_params'])
        _methods = ",\n".join(value['methods'])
        _remarks = '\n'.join(wrap(value['remarks'], 30))
        _data.append([_function, _path_params, _methods, _remarks])

    table_data.extend(_data)
    table_instance = AsciiTable(table_data)
    table_instance.inner_heading_row_border = True
    table_instance.inner_row_border = True
    return table_instance
