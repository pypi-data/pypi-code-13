from terminaltables import AsciiTable
from textwrap import wrap
from .sently_resource_mapping import RESOURCE_MAPPING

def printinfo():
    table_data = [['Function', 'Description', 'Methods']]
    max_width = 30
    table_data.extend([[key, value['resource'] + "\n" + '\n'.join(wrap(value['description'], max_width)), value['methods']] for key, value in RESOURCE_MAPPING.items()])
    table_instance = AsciiTable(table_data)
    table_instance.inner_heading_row_border = True
    table_instance.inner_row_border = True
    print(table_instance.table)
