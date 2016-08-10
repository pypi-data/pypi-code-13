import os
import pdb

''' 
    walk_funcs.py

    Functions to run on each node in the tree. 
'''

def create_file(path, node):

    file_to_create = os.path.join(path, node['value'])
    if node['children'] is None:
        # leaf, regular file
        open(file_to_create,'w')
    else:
        # node, directory
        os.mkdir(file_to_create)

def make_line_printer(indent, indent_char=' '):
    ''' Make a function that prints out each node as a file or directory and indents accordingly. '''

    def _print_line(node, level=0):

        line = node['value']
        if node['children'] is not None:
            line += '/'

        print (indent_char * level * indent) + line

    return _print_line


